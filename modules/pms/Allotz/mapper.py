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
        """Allots API can returna short date ie 2018-05-05, this will covert to the
        LG Pro:Centric accepted date for mate of 2018-05-05T00:00:00+12:00
        """
        return date + 'T00:00:00+12:00'


class Mapper(object):

    @staticmethod
    def get_rooms():
        allotz = connector.Allotz(property_id=2404,
                        key_1='a21b5217577bc770cda9df2173e8a954',
                        key_2='c34d39bd3133a0e1af4bb7266bf04223')

        #allotz = Allotz(property_id=968, key_1='e375f729ecf58e9f882e1c32014049f8', key_2='5c7dc96ee3fe1334b495fc665e6e085d')
        #query = ("?checkin_data_gte=%s" % datetime.now().strftime("%Y-%m-%d"))
        query = '?'
        rooms = allotz.get_bookings(query=query)
        return Mapper.map_rooms(rooms)

    @staticmethod
    def map_rooms(rooms):
        try:
            data = {}
            for items in rooms['bookings']:

                for room in items['rooms']:

                    if room['occupation_status'] == 'checked_in':
                        room['occupation_status'] = 'true'
                    else:
                        room['occupation_status'] = 'false'

                    # temp_token is added as dic will not allow repetitive keys, this is remove before
                    # it is sent on to Pro:Centric via the XML parser.

                    data['room lastUpdate="' + Helper.fix_long_date(items['updated_at']) + '" temp_token=' + room['room_number']] = {
                        'roomID': room['room_number'],
                        'guest': {
                            "firstName": "null",
                            "lastName": room['guest_name'],
                            "salutation": "null",
                            "langcode": "en_GB",
                            "checkIn": Helper.fix_short_date(room['checkin_date']),
                            "scheduledCheckOut": Helper.fix_short_date(room['checkout_date']),
                            "checkInStatus": room['occupation_status'],
                        },

                    }
            return data

        except KeyError:
            exit()

    @staticmethod
    def get_room(room_no):
        print(room_no)
        allotz = Allotz(property_id=2404,
                        key_1='a21b5217577bc770cda9df2173e8a954',
                        key_2='c34d39bd3133a0e1af4bb7266bf04223')

        #allotz = Allotz(property_id=968, key_1='e375f729ecf58e9f882e1c32014049f8', key_2='5c7dc96ee3fe1334b495fc665e6e085d')
        #query = ("?checkin_data_gte=%s" % datetime.now().strftime("%Y-%m-%d"))
        query = '?'
        rooms = allotz.get_bookings(query=query)
        return Mapper.map_room(rooms, room_no)

    @staticmethod
    def map_room(rooms, room_no):
        """ Map single room for Pro:Centric v2 API"""
        try:
            data = {}
            for items in rooms['bookings']:
                for room in items['rooms']:
                    if room['room_number'] == str(room_no):

                        if room['occupation_status'] == 'checked_in':
                            room['occupation_status'] = True
                        else:
                            room['occupation_status'] = False

                        data['status'] = 'success'
                        data['data'] = {
                            'id': room['room_id'],
                            'guest': {
                                'name': {
                                    'prefix': 'null',
                                    'first': 'null',
                                    'middle': 'null',
                                    'last': 'null',
                                    'suffix': 'null',
                                    'full': room['guest_name']
                                },
                                'balance': 'null',
                                'language': 'null',
                                'no_post': 'null',
                                'vip_status': 'null',
                                'id': '101-2',
                                'option': 'null',
                                'channel_preference': 'null',
                            }
                        }
                        Log.objects.create(level="N", output="MAPPING :: SUCCESS")
                    else:
                        data['status'] = 'success'
                        data['data'] = {}
                        Log.objects.create(level="E", output="MAPPING :: FAILED")
            return data

        except KeyError:
            exit()

