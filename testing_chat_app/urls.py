from django.contrib import admin
from django.urls import path, include

from chat.views import (index, send_message_to_friend, send_friend_request,
                        response_friend_request, cancel_friend_request, remove_friend)

urlpatterns = [
    path('accounts/', include('allauth.urls')),
    path('admin/', admin.site.urls),
    path('chat/', include('chat.urls')),
    path('api/', include('drf_api.urls')),
    path('', index, name='index'),
    path('send-message-to-friend/', send_message_to_friend, name='send-message-to-friend'),
    path('send-friend-request/', send_friend_request, name='send-friend-request'),
    path('cancel-friend-request/', cancel_friend_request, name = 'cancel-friend-request'),
    path('response-friend-request/', response_friend_request, name='response-friend-request'),
    path('remove-friend/', remove_friend, name='remove-friend'),
]
