from django.urls import include, re_path, path
from procentric_connect.views import *

urlpatterns = [

    #path('', views.index, name='index'),


    # Url pattern for Pro:Centric TwoWay PMS API
    re_path(r'^pms/v2/check', PMS2WayCheck.as_view(), name='check'),
    re_path(r'^pms/v2/details',PMS2WayDetails.as_view(), name='details'),
    #re_path(r'^pms/v2/host',PMS2WayHost.as_view(), name=host),
    #re_path(r'^pms/v2/site',PMS2WaySite.as_view(), name='site'),
    re_path(r'^pms/v2/statuses', PMS2WayStatus.as_view(), name='statuses'),
    path(r'pms/v2/rooms/<room_id>',PMS2WayRoom.as_view(), name='details'),
    path(r'pms/v2/rooms/<room_id>/folios/<guest_id>',PMS2WayFolios.as_view(), name='folios'),

    re_path(r'^pms/v2/subscriptions',PMS2WaySubscriptions.as_view(), name='subscriptions'),

    #re_path(r'^pms/v2/init',PMS2WayInit.as_view(), name='init),

    # Url pattern for Pro:Centric Webhooks.
    re_path(r'^pms/v2/webhooks/checkin', PMS2WayWebhooks.as_view(), name='checkin'),
    re_path(r'^pms/v2/webhooks/checkout', PMS2WayWebhooks.as_view(), name='checkout'),
    re_path(r'^pms/v2/webhooks/moveroom', PMS2WayWebhooks.as_view(), name='moveroom'),
    re_path(r'^pms/v2/webhooks/getrooms', PMS2WayWebhooks.as_view(), name='getrooms'),
    re_path(r'^pms/v2/webhooks/update', PMS2WayWebhooks.as_view(), name='update'),
]