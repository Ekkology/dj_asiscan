import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import dj_asiscan.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dj_asiscan.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            dj_asiscan.routing.websocket_urlpatterns
        )
    ),
})
