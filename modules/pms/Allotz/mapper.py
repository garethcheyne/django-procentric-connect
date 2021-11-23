import json
from datetime import datetime
from procentric_connect.modules.pms.Allotz import connector



class Helper(object):
    @staticmethod
    def fix_long_date(date):
        """Allots API can returns a long date, but we need to remove the seconds from it
        so it can be accepted by LG Pro:Centric.
        """
        return date[:19] + date[(19+4):]

    @staticmethod
    def fix_short_date(date):
        """Allots API can return a short date ie 2018-05-05, this will covert to the
        LG Pro:Centric accepted date for mate of 2018-05-05T00:00:00+12:00
        """
        return date + 'T00:00:00+12:00'


class Mapper(object):


    @staticmethod
    def get_details():
        
        allotz = connector.Allotz()

        payload = {
            "status": "success",
            "data":{
                "id": allotz.property_id,
                "name": allotz.property_name,
                "currency":"NZD",
                "website": "https://www.hiddenlakehotel.co.nz",
                "timezone":"NZT",
                "timestamp": datetime.now().isoformat(),
                "status": "up",
                "suscriptionId": 1
            }
        }
        return payload

    @staticmethod
    def get_room(room_no):
        allotz = connector.Allotz()
        query = ("?checkout_data_gte=%s&checkin_date_lte=%s" % (datetime.now().strftime("%Y-%m-%d"), datetime.now().strftime("%Y-%m-%d")))
        bookings = allotz.get_bookings(query)
        room = Mapper.map_room(bookings, room_no)
        return room

    @staticmethod
    def get_folios(room_id, guest_id):
        allotz = connector.Allotz()
        query = ("?checkout_data_gte=%s&checkin_date_lte=%s" % (datetime.now().strftime("%Y-%m-%d"), datetime.now().strftime("%Y-%m-%d")))
        bookings = allotz.get_bookings(query)
        folios = Mapper.map_folios(bookings, room_id, guest_id)
        return folios


    @staticmethod
    def map_folios(bookings, room_id, guest_id):
        """ Map single rooms folio charges fro Pro:CEntric v2 API"""
        print(room_id)
        try:
            balance = 0.00
            payload = {}


            for booking in bookings['bookings']:
                for room in booking['rooms']:
                    if room['room_number'] == str(room_id):
                        if room['occupation_status'] == 'checked_in':
                            pass
                        else:
                            continue                    
                        
                        if 'extras' in booking:
                            payload['items'] = []

                            for extra in booking['extras']:
                                payload['items'].append({
                                    'id': extra['id'],
                                    'created': Helper.fix_short_date(extra['sell_date']),
                                    'description': str(extra['count']) +'x - ' + extra['title'],
                                    'amount': float(extra['total']),
                                    'display': True
                                })

                                balance += float(extra['total'])

                        payload['id'] = room['id']
                        payload['status'] = 'open'
                        payload['balance'] = balance

            return payload

        except KeyError:
            exit()



    @staticmethod
    def map_room(bookings, room_no):
        """ Map single room for Pro:Centric v2 API"""
        try:
            payload = {
                'status': 'success',
                'data': {}
                }

            for booking in bookings['bookings']:
                for room in booking['rooms']:
                    if room['room_number'] == str(room_no):
                        if room['occupation_status'] == 'checked_in':
                            pass
                        else:
                            continue
                        
                        payload['data'] = {
                            'id': str(room['id']),
                            'guests':[{ 
                                'name': {
                                    'full': room['guest_name']
                                },
                                'balance': booking['due'],
                                'language': None,
                                'no_post': None,
                                'vip_status': None,
                                'id':str(room['guest']['id']),
                                'option': None,
                                'channel_preference': None,
                                }
                            ]
                        }
                        #Log.objects.create(level="N", output="MAPPING :: SUCCESS")
                    else:
                        continue
                        #Log.objects.create(level="E", output="MAPPING :: FAILED")
            return payload

        except KeyError:
            exit()

