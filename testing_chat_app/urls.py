from django.contrib import admin
from django.urls import path, include

from chat.views import index, send_message_to_friend, send_friend_request

urlpatterns = [
    path('admin/', admin.site.urls),
    path('chat/', include('chat.urls')),
    path('', index, name='index'),
    path('send-message-to-friend/', send_message_to_friend, name='send-message-to-friend'),
    path('send-friend-request/', send_friend_request, name='send-friend-request'),

]
