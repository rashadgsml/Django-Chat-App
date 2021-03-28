from rest_framework import serializers
from chat.models import Profile, Chat, Notification, Message
from django.contrib.auth.models import User

class ProfileSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source="user.username")
    
    class Meta:
        model = Profile
        fields = (
            'id','user','friends','friend_requests','status'
        )

class MessageSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source="author.username")
    
    class Meta:
        model = Message
        fields = (
            'author','content','timestamp'
        )

class ChatSerializer(serializers.ModelSerializer):
    participants = ProfileSerializer(many=True)
    messages = MessageSerializer(many=True)
    
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