# Simple Class Method for collecting room information from AllotzAPI API
import sys
import requests
import json
import os


class Allotz(object):
    """A customer API class to interact with the Allotz API to PMS API""" 

    def __init__(self):
        with open(os.getcwd() + "/secrets.json") as fp:
            settings = json.load(fp)       

        self.property_id = settings["allotz_pms"]["property_id"]
        self.property_name = settings["allotz_pms"]["property_name"]
        self.key_1 = settings["allotz_pms"]["public_key"]
        self.key_2 = settings["allotz_pms"]["private_key"]
        self.uri = settings["allotz_pms"]["base_url"]


        #Log.objects.create(level='N', output='REQUEST :: PENDING : Requesting Token form Allotz.com')
        r = requests.post(url=(self.uri + "%s/token/?key1=%s&key2=%s" % (self.property_id, self.key_1, self.key_2)))
        if r.status_code is 200:
            self.session = requests.Session()
            self.session.headers.update({'x-api-token': r.json()['token']})
            print('Allots Access token.')
            print(r.json()['token'])
            print('\n')
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


    def get_room(self, room_id=None):

        r = self.session.get(url=self.uri + ("%s/rooms/%s" % (self.property_id, room_id)))
        if r.status_code is 200:
            print(r.json())
            return r.json()
        elif r.status_code is 404:
            raise ValueError('Access Denied, response = 404')
        return


    def get_rooms(self):
        r = self.session.get(url=self.uri + "%s/rooms" % (self.property_id))
        if r.status_code is 200:
            print(r.json())
            return
        elif r.status_code is 404:
            raise ValueError('Access Denied, response = 404')
        return


    def get_extras(self, query=None):
        if query is None:
            query = '?'
        r = self.session.get(url=self.uri + ("%s/extras%s" % (self.property_id, query)))
        return r.json()
