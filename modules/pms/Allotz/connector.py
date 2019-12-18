# Simple Class Method for collecting room information from AllotzAPI API
import sys
import requests

class Allotz(object):
    """A customer API class to interact with the AllotzAPI PMS API"""

    # Keys for AllotzAPI test platform.
    _key_1 = 'e375f729ecf58e9f882e1c32014049f8'
    _key_2 = '5c7dc96ee3fe1334b495fc665e6e085d'

    def __init__(self, property_id, key_1, key_2):
        self.property_id = property_id
        self.key_1 = key_1
        self.key_2 = key_2
        self.uri = 'https://frontdesk.allotz.com/api/public/v1/openapi/'

        #Log.objects.create(level='N', output='REQUEST :: PENDING : Requesting Token form Allotz.com')
        r = requests.post(url=(self.uri + "%s/token/?key1=%s&key2=%s" % (self.property_id, self.key_1, self.key_2)))
        if r.status_code is 200:
            self.session = requests.Session()
            self.session.headers.update({'x-api-token': r.json()['token']})
            #Log.objects.create(level="N", output="REQUEST :: SUCCESS")
        elif r.status_code is 404:
            #Log.objects.create(level="E", output="REQUEST :: ERROR : 404/Access Denied")
            raise ValueError('Access Denied, response = 404')
        else:
            exit()

    def __str__(self):
        return

    def get_bookings(self, query=None):
        if query is None:
            query = '?'
        r = self.session.get(url=self.uri + ("%s/bookings%s" % (self.property_id, query)))
        if r.status_code is 200:
            return r.json()
        elif r.status_code is 404:
            raise ValueError('Access Denied, response = 404')
        return

    def get_extras(self, query=None):
        if query is None:
            query = '?'
        r = self.session.get(url=self.uri + ("%s/extras%s" % (self.property_id, query)))
        return r.json()
