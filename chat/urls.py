# chat/urls.py
from django.urls import path

from .views import chat_index, room

app_name = 'chat'

urlpatterns = [
    path('', chat_index, name='chat_index'),
    path('<str:room_name>/', room, name='room'),
]