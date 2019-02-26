from django.conf.urls import url
#from channels.routing import ChannelNameRouter, ProtocolTypeRouter, URLRouter
from . import consumers

websocket_urlpatterns = [
    url(r'^ws/chat/(?P<room_name>[^/]+)/$', consumers.ChatConsumer),
]

#application = ProtocolTypeRouter({
#    "websocket": URLRouter([
#        url(r'^ws/chat/(?P<room_name>[^/]+)/$', consumers.ChatConsumer),
#    ]),
#    "channel": ChannelNameRouter({
#        "stock_bot": consumers.GenerateConsumer,
#    }),
#})
