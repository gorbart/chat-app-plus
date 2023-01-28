"""
ASGI config for chatappplus project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/asgi/
"""

import os

from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from django.core.asgi import get_asgi_application

from chat import urls
from .channelsmiddleware import JWTAuthMiddlewareStack

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chatappplus.settings')

application = ProtocolTypeRouter({
    "http":
        get_asgi_application(),
    "websocket":
        AllowedHostsOriginValidator(
            JWTAuthMiddlewareStack(URLRouter(urls.websocket_urlpatterns))),
})
