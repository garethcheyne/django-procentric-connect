from django.shortcuts import render
from django.http import JsonResponse

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from procentric_connect.renderers.PCDXMLRenderer import PCDXML

#_temp need to figure out how to selected this module to use from admin menu.
from procentric_connect.modules.pms.Allotz.mapper import Mapper


# Create your views here.
class PMSOneWay(APIView):
    """API for Pro:Centric OneWay"""

    #permission_classes = (IsAuthenticated, )
    renderer_classes = (PCDXML, )

    def get(self, request):
        print("ProCentric-Connect :: PCD requested update.")
        if self.request.method == 'GET':
            self.response = Mapper.get_rooms()
            return Response(self.response, status=200)
        else:
            return Response({}, status=400)


class PMS2WayCheck(APIView):
    """Check API for Pro:Centric TwoWay """

    def post(self, request):
        # This is in NO WAY SECURE, it just a flat response to get started.
        print("ProCentric Connect :: API check request")
        print(request.method)
        print(request.headers)
        print(request.body)
        data = {'status': 'success'}
        print("ProCentric Connect :: API check response")
        return JsonResponse(data, status=200)

class PMS2WayStatus(APIView):
    """Status API for Pro:Centric TwoWay """

    def get(self, request):
        print("ProCentric Connect :: API status request")
        print(request.method)
        print(request.headers)
        print(request.body)
        self.body = {'status': 'success'}

        print("ProCentric Connect :: API status response")
        return JsonResponse(self.body, status=200)
            
class PMS2WayDetail(APIView):
    """Details API for Pro:Centric TwoWay """

    def get(self):
        print("ProCentric Connect :: API details request")
        print(self.request.method)
        print(self.request.headers)
        print(self.request.body)
        if self.request.method == "GET":
            self.body = ProCentricPMS.get_details(request.body)
            print("ProCentric Connect :: API details response")
            return JsonResponse(self.body, status=200)
        else:
            return JsonResponse({}, status=404)