from channels.auth import AuthMiddlewareStack
from channels.routing import ChannelNameRouter, ProtocolTypeRouter, URLRouter
import chat.routing


application = ProtocolTypeRouter({
    # (http->django views is added by default)
    'websocket': AuthMiddlewareStack(
        URLRouter(
            chat.routing.websocket_urlpatterns
        )
    ),
    'channel': ChannelNameRouter({
        'stockbot': chat.consumers.StockConsumer,
    }),
})

#application = ProtocolTypeRouter({
#    "websocket": URLRouter([
#        url(r'^ws/chat/(?P<room_name>[^/]+)/$', consumers.ChatConsumer),
#    ]),
#    "channel": ChannelNameRouter({
#        "stock_bot": consumers.GenerateConsumer,
#    }),
#})

