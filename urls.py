from django.urls import include, re_path
from procentric_connect.views import *

urlpatterns = [

    # Url pattern for Pro:Centric OneWay PMS API
    re_path(r'^pcs/', PMSOneWay.as_view()),

    # Url pattern for Pro:Centric TwoWay PMS API
    re_path(r'^pms/v2/check', PMS2WayCheck.as_view(), name='check'),
    re_path(r'^pms/v2/statuses', PMS2WayStatus.as_view(), name='status'),
    re_path(r'^pms/v2/details',PMS2WayDetail.as_view(), name='details'),

]