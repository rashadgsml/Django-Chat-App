# chat/routing.py
from django.urls import re_path
from .consumers import ChatConsumer, NotificationConsumer


websocket_urlpatterns = [
    re_path(r'ws/chat/(?P<room_name>\w+)/$', ChatConsumer.as_asgi()),
    re_path(r'', NotificationConsumer.as_asgi()),
]