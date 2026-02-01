"""
ASGI config for chatapp project.

It exposes the ASGI callable as a module-level variable named ``application``.
"""

import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import groupchat.routing  # Your app routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chatapp.settings')

# Standard Django ASGI application for HTTP
django_asgi_app = get_asgi_application()

# Main ASGI application supporting HTTP + WebSockets
application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket": AuthMiddlewareStack(
        URLRouter(
            groupchat.routing.websocket_urlpatterns
        )
    ),
})
