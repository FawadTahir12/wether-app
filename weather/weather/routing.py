from channels.auth import AuthMiddlewareStack
from django.core.asgi import get_asgi_application
from channels.routing import URLRouter, ProtocolTypeRouter
import app.routing

application = ProtocolTypeRouter({
    'http': get_asgi_application(),
    'websocket': AuthMiddlewareStack(
       URLRouter(
           app.routing.websocket_urlpatterns
       )
    ),
})