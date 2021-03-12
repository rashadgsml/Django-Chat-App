from django.core.asgi import get_asgi_application
django_asgi_app = get_asgi_application()
import chat.routing
import os
import django

from django.conf.urls import url


# Fetch Django ASGI application early to ensure AppRegistry is populated
# before importing consumers and AuthMiddlewareStack that may import ORM
# models.
os.environ['DJANGO_SETTINGS_MODULE'] = 'testing_chat_app.settings'

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
django.setup()
application = ProtocolTypeRouter({
    # Django's ASGI application to handle traditional HTTP requests
    "http": django_asgi_app,

    # WebSocket chat handler
    "websocket": AuthMiddlewareStack(
        URLRouter(
            chat.routing.websocket_urlpatterns
        )
    ),
})