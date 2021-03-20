from django.urls import path
from .views import ChatList, ChatDetail, ProfileList, ProfileDetail

app_name = 'drf_api'

urlpatterns = [
    path('chat-list/', ChatList.as_view(), name = 'chat-list'),
    path('profile-list/', ProfileList.as_view(), name = 'profile-list'),
    path('chat-detail/<str:pk>', ChatDetail.as_view(), name = 'chat-detail'),
    path('profile-detail/<str:pk>', ProfileDetail.as_view(), name = 'profile-detail'),

]
