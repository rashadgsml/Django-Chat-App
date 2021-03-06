# chat/consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer, WebsocketConsumer
from asgiref.sync import async_to_sync
from .models import Message, Chat, Profile, FriendRequest
from core.models import Notification
from django.contrib.auth import get_user_model
from channels.layers import get_channel_layer


User = get_user_model()

class NotificationConsumer(WebsocketConsumer):

    def notify(self, event):
        message = event['message']
        if self.scope["user"].username==message['to']:
            self.send(text_data=json.dumps(message))

    def send_message_notification(self, data):
        async_to_sync(self.channel_layer.group_send)(
            'notifications',
            {
                'type': 'notify',
                'message': data,
            }
        )

    def send_friend_request(self, data):
        my_profile = Profile.objects.get(user=self.scope["user"])
        to_user = User.objects.get(id=int(data['to_id']))
        to_profile = Profile.objects.get(user=to_user)
        Notification.objects.create(from_profile=my_profile,to_profile=to_profile,content='has sent you friend request')
        friend_request_qs = FriendRequest.objects.filter(from_profile=my_profile,to_profile=to_profile)
        if not friend_request_qs.exists():
            friend_request = FriendRequest.objects.create(from_profile=my_profile, to_profile=to_profile)
            to_profile.friend_requests.add(friend_request)
            my_profile.friend_requests.add(friend_request)

    def cancel_friend_request(self, data):
        my_profile = Profile.objects.get(user=self.scope["user"])
        to_user = User.objects.get(id=int(data['to_id']))
        to_profile = Profile.objects.get(user=to_user)
        FriendRequest.objects.filter(from_profile=my_profile,to_profile=to_profile).delete()
        Notification.objects.filter(from_profile=my_profile,to_profile=to_profile,content='has sent you friend request').delete()

    def connect(self):
        profile = Profile.objects.get(user=self.scope["user"])
        profile.status = 'online'
        profile.save()
        async_to_sync(self.channel_layer.group_add)(
            'notifications',
            self.channel_name,
        )
        self.accept()

    def disconnect(self, close_code):
        profile = Profile.objects.get(user=self.scope["user"])
        profile.status = 'offline'
        profile.save()
        async_to_sync(self.channel_layer.group_discard)(
            'notifications',
            self.channel_name
        )

    commands = {
        'message_notification':send_message_notification,
        'send_friend_request': send_friend_request,
        'cancel_friend_request': cancel_friend_request,
    }

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        try:
            self.commands[text_data_json['command']](self, text_data_json)
        except:
            pass
        

    def notifications_to_json(self,notifications):
        result = []
        for notification in notifications:
            result.append(self.notification_to_json(notification))

        return result

    def notification_to_json(self,notification):
        return {
            'to_profile': notification.to_profile.user.username,
            'from_profile': notification.message.author.username,
            'message': notification.message.content,
            'timestamp': str(notification.message.timestamp),
            'is_read': notification.is_read
        }
        

class ChatConsumer(WebsocketConsumer):

    def fetch_messages(self, data):
        chat = Chat.objects.get(room_name=data['room_name'])
        messages = chat.last_10_messages()
        content = {
            'command': 'messages',
            'messages': self.messages_to_json(messages)
        }
        profile = Profile.objects.get(user=self.scope["user"])
        profile.status = 'online'
        rooms = Chat.objects.filter(participants=profile)
        content['rooms'] = self.rooms_to_json(rooms)
        self.send_message(content)
    
    def new_message(self, data):
        author = data['from']
        author_user = User.objects.filter(username=author)[0]
        
        message = Message.objects.create(
            author = author_user,
            content = data['message']
        )
        
        content = {
            'command': 'new_message',
            'message': self.message_to_json(message),
        }
        chat = Chat.objects.get(room_name=data['room_name'])
        chat.messages.add(message)
        all_rooms = Chat.objects.all()
        content['all_rooms'] = self.rooms_to_json(all_rooms)
        return self.send_chat_message(content)

    def messages_to_json(self, messages):
        result = []
        for message in messages:
            result.append(self.message_to_json(message))
        return result
        
    def message_to_json(self, message):
        return {
            'author': message.author.username,
            'content': message.content,
            'timestamp': str(message.timestamp)
        }

    def rooms_to_json(self, rooms):
        result = []
        for room in rooms:
            result.append(self.room_to_json(room))
        return result
        
    def room_to_json(self, room):
        return {
            'room_id': room.id,
            'room_name': room.room_name,
            'participants': self.participants_to_json(room.participants.all()),
            'messages': self.messages_to_json(room.messages.all())
        }

    def participants_to_json(self, participants):
        result = []
        for participant in participants:
            result.append(self.participant_to_json(participant))
        return result
        
    def participant_to_json(self, participant):
        return {
            'username': participant.user.username,
            'status': participant.status
        }

    commands = {
        'fetch_messages': fetch_messages,
        'new_message': new_message,
    }

    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name
        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name,
        )
        self.accept()
        
    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )
        
    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        self.commands[text_data_json['command']](self, text_data_json)

    def send_chat_message(self, message):
        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
            }
        )
        
    def send_message(self, message):
        self.send(text_data=json.dumps(message))

    # Receive message from room group
    def chat_message(self, event):
        message = event['message']
        # Send message to WebSocket
        self.send(text_data=json.dumps(message))


