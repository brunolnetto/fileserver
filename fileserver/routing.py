
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from web.routing import websocket_urlpatterns


websocket_config = {
    'websocket': AuthMiddlewareStack(URLRouter(websocket_urlpatterns)),
}

application = ProtocolTypeRouter(websocket_config)