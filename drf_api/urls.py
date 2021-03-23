from django.urls import path
from .views import ChatList, ChatDetail, ProfileList, ProfileDetail, NotificationList, NotificationDetail

app_name = 'drf_api'

urlpatterns = [
    path('chat-list/', ChatList.as_view(), name = 'chat-list'),
    path('profile-list/', ProfileList.as_view(), name = 'profile-list'),
    path('notification-list', NotificationList.as_view(), name = 'notification-list'),
    path('chat-detail/<str:pk>', ChatDetail.as_view(), name = 'chat-detail'),
    path('profile-detail/<str:pk>', ProfileDetail.as_view(), name = 'profile-detail'),
    path('notification-detail/<str:pk>', NotificationDetail.as_view(), name = 'notification-detail'),
    
]
