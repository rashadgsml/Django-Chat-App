from rest_framework import serializers
from chat.models import Profile, Chat, Notification
from django.contrib.auth.models import User

class ProfileSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source="user.username")
    
    class Meta:
        model = Profile
        fields = (
            'id','user','friends','friend_requests','status'
        )

class ChatSerializer(serializers.ModelSerializer):
    participants = ProfileSerializer(many=True)

    class Meta:
        model = Chat
        fields = (
            'id','room_name','participants','messages'
        )

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = (
            'id', 'to_profile', 'message','is_read'
            )