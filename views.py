import json
import requests
from django.shortcuts import render
from django.http import JsonResponse
from datetime import datetime


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from pprint import pprint

#_temp need to figure out how to selected this module to use from admin menu.
from procentric_connect.modules.pms.Allotz.mapper import Mapper

fake_guest = {
    'status': 'success', 
    'data': {
        'id': '202',
        'guests': [{
            'name': {
                'full': 'Glenda Hamilton'
                }, 
            'balance': None, 
            'language': None, 
            'no_post': None, 
            'vip_status': None, 
            'id': '202-3', 
            'option': None, 
            'channel_preference': None
            }]
            }
            }
            


class PMS2WayCheck(APIView):
    """Check API for Pro:Centric TwoWay """

    def post(self, request):
        # This is in NO WAY SECURE, it just a flat response to get started.
        print("\n=============================================")
        print("ProCentric Server :: API check request \n") 
     
        payload = {
            'status': 'success'
            }

        print("ProCentric Connect :: API check response")
        print("=============================================")
        return JsonResponse(payload, status=200)


class PMS2WayDetails(APIView):
    """Details API for Pro:Centric TwoWay"""

    def get(self, request):
        print("\n=============================================")
        print("ProCentric Connect :: API details request \n")        

        data = Mapper.get_details()

        print("ProCentric Connect :: API details response")
        print("=============================================")
        return JsonResponse(data, status=200)

class PMS2WayStatus(APIView):
    """Status API for Pro:Centric TwoWay """

    def get(self, request):
        print("=============================================")
        print("ProCentric Connect :: API status request")
        body = {
            "status": "success",
            "data":{
                "id": "1801",
                "created": datetime.now().isoformat(),
                "status": "up"
                }
            }
        print(body)

        print("ProCentric Connect :: API status response")
        print("=============================================")
        return JsonResponse(body, status=200)
            
            
class PMS2WayRoom(APIView):
    """Rooms API for Pro:Centric TwoWay """

    def get(self, request, room_id):
        print("\n=============================================")
        print("ProCentric Connect :: API-PMS2Way Room \n")        

        if self.request.method == "GET":

            headers = 'application/json'

            payload = None
            status = None
                     
            payload = Mapper.get_room(room_id)

            print(payload)
            
            # If no guest in room return 404 as per ProCentric Documentation
            if 'id' in payload['data']:
                status = 200
            else:
                payload = None
                status = 404

            print("\nProCentric Connect :: API-PMS2Way Room-Response")
            return JsonResponse(data=payload, content_type=headers, safe=False, status=status)
        else:
            print("=============================================")
            return JsonResponse({}, status=404)

class PMS2WayFolios(APIView):
    """Rooms API for Pro:Centric TwoWay """

    def get(self, request, room_id, guest_id):
        print("\n=============================================")
        print("ProCentric Connect :: API-PMS2Way Folios \n")  
   
        if self.request.method == "GET":

            headers = 'application/json'

            payload = None
            status = None
                       
            payload = Mapper.get_folios(room_id, guest_id)

            
            # If no folios in room return 404 as per ProCentric Documentation
            if len(payload) is not 0:
                status = 200
            else:
                payload = None
                status = 404

            print("\nProCentric Connect :: API-PMS2Way Folios - Response")
            return JsonResponse(data=payload, content_type=headers, safe=False, status=status)
        else:
            print("=============================================")
            return JsonResponse({}, status=404)            

class PMS2WaySubscriptions(APIView):
    """Subscriptions API for Pro:Centric TwoWay """

    def post(self, request):
        print("=============================================")
        print("ProCentric Connect :: API subscriptions request")

        if self.request.method == "POST":
            request.body = json.loads(request.body.decode('utf-8'))

            token = request.body['callbackToken']
            uri = request.body['callbackUri']

            print(uri)

            body = {
                "status": "success"
            }


            print("ProCentric Connect :: API subscriptions response")
            print("=============================================")
            return JsonResponse(body, status=200)
        else:
            print("=============================================")
            return JsonResponse({}, status=404)



class PMS2WayWebhooks(APIView):

    def post(self, request):
        print("=============================================")
        print("ProCentric Connect :: API WebHooks")

        if self.request.method == "POST":
            request.body = json.loads(request.body.decode('utf-8'))
            print(request.body)

            hook = self.request.path.split("/")[5]

            room_no = ""
            room_no = self.request.path.split("/")[6]

            response = {}
            print(hook)

            if hook == "checkin":
                print("Checked In Room " + room_no)

                response = self.check_in(room_no)

            elif hook == "checkout":
                response = self.check_out(room_no)

            elif hook == "moveroom":
                pass

            elif hook == "getrooms":
                response = self.get_rooms()

            elif hook == "update":
                response = self.update(request.body)          

            
            return JsonResponse(response, status=200)
        else:
            print("=============================================")
            return JsonResponse({}, status=404)


    def get_token(self):
        """Subscriptions API for Pro:Centric TwoWay """
        url = "https://192.168.1.15:60080/api/v2/auth/tokens"
        payload = "{\n\t\"client_id\": \"admin\",\n\t\"client_secret\": \"Ribl#t19bo!!\",\n\t\"grant_type\": \"client_credentials\"\n\t\n}"
        headers = {
                'content-type': "application/json",
                'cache-control': "no-cache",
                }

        response = requests.request("POST", url, verify=False, data=payload, headers=headers).json()

        return "Bearer " + str(response['access_token'])

    def get_rooms(self):
        Mapper.get_rooms()
        return

    def check_in(self, room_no):
        token = self.get_token()
        url = "https://192.168.1.15:60080/api/v2/events/pms"
        headers = {'Authorization': token}

        payload = {
            "data":{
                "events":[{
                    "type": "checkin",
                    "checkin":{
                        "room": room_no
                    },
                }]
            }
        }     
        print(payload)                       
                            
        request = requests.request("POST", url, verify=False, json=payload, headers=headers)
        print("\nProCentric Server :: Response =", format(request.text))

        if request.status_code is 200:
            return {"status": "success"}
        else:
            return {"status": "failed"}

    def check_out(self, room_no):
        token = self.get_token()
        url = "https://192.168.1.15:60080/api/v2/events/pms"
        headers = {'Authorization': token}

        payload = {
            "data":{
                "events":[{
                    "type": "checkout",
                    "created": datetime.now().isoformat(),
                    "checkout":{
                        "id": room_no,
                        "room": room_no,
                    },
                }]
            }
        }
        print(payload)                            
                            
        request = requests.request("POST", url, verify=False, json=payload, headers=headers)
        print("\nProCentric Server :: Response =", format(request.text))

        if request.status_code is 200:
            return {"status": "success"}
        else:
            return {"status": "failed"}


    def update(self, body):
        token = self.get_token()
        url = "https://192.168.1.15:60080/api/v2/events/pms"
        headers = {'Authorization': token}

        payload = {
            "data":{
                "events":[{
                    "type": "update",
                    "checkin":{
                        "room": body['room_no']
                    },
                }]
            }
        }     
        print(payload)                       
                            
        request = requests.request("POST", url, verify=False, json=payload, headers=headers)
        print("\nProCentric Server :: Response =", format(request.text))

        if request.status_code is 200:
            return {"status": "success"}
        else:
            return {"status": "failed"}

