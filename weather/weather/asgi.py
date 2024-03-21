"""
ASGI config for weather project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application
from channels.routing import URLRouter, ProtocolTypeRouter
from channels.auth import AuthMiddlewareStack
import app.routing
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "weather.settings")

# application = get_asgi_application()

# application = ProtocolTypeRouter({
#     'http': get_asgi_application(),
#     'websocket': AuthMiddlewareStack(URLRouter(app.routing.websocket_urlpatterns))
# })
