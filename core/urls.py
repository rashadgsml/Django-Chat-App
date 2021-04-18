from django.urls import path
from django.contrib.auth.decorators import login_required
from .views import (index, send_message_to_friend, send_friend_request,friends,notifications,
                    response_friend_request, cancel_friend_request, remove_friend,CreatePostView)

app_name = 'core'

urlpatterns = [
    path('', index, name='index'),
    path('send-message-to-friend/', send_message_to_friend, name='send-message-to-friend'),
    path('send-friend-request/', send_friend_request, name='send-friend-request'),
    path('cancel-friend-request/', cancel_friend_request, name = 'cancel-friend-request'),
    path('response-friend-request/', response_friend_request, name='response-friend-request'),
    path('remove-friend/', remove_friend, name='remove-friend'),
    path('new-post/', login_required(CreatePostView.as_view()), name='new-post'),
    path('friends/',friends,name='friends'),
    path('notifications/',notifications,name='notifications'),
]