from django.shortcuts import render, redirect, reverse
from django.contrib.auth.decorators import login_required
from django.utils.safestring import mark_safe
from .models import Message, Chat, Profile, FriendRequest
import json
from django.contrib.auth import get_user_model
import random
import string

User = get_user_model()

def index(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    profiles = Profile.objects.all()
    friend_requests = FriendRequest.objects.filter(to_profile=profile).all()
    context = {
        'profile': profile,
        'profiles': profiles,
        'friend_requests': friend_requests
    }
    return render(request, 'index.html', context)

@login_required
def send_friend_request(request):
    user_data = request.POST.get('user')
    the_user = User.objects.get(username = user_data)

    user_profile = Profile.objects.get(user=the_user)
    my_profile = Profile.objects.get(user=request.user)

    friend_request = FriendRequest.objects.create(from_profile=my_profile, to_profile=user_profile)
    
    # TODO: friend request successfully sent
    return redirect('index')


def send_message_to_friend(request):
    friend_data = request.POST.get('friend')
    friend_user = User.objects.get(username = friend_data)
    profile, created = Profile.objects.get_or_create(user=request.user)
    friend = Profile.objects.get(user=friend_user)
    room_qs = Chat.objects.filter(participants=profile).filter(participants=friend)
    if room_qs.exists():
        for i in room_qs:
            if i.participants.all().count() == 2:
                room = i
                return redirect('/chat/{}'.format(room.room_name))

    room = Chat.objects.create(room_name=get_random_value())
    room.participants.add(profile)
    room.participants.add(friend)
    return redirect('chat:room', room_name=room.room_name)
    
def get_random_value():
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=10))

def chat_index(request):
    return render(request, 'chat/index.html')

@login_required
def room(request, room_name):
    chat, created = Chat.objects.get_or_create(room_name=room_name)
    profile, created = Profile.objects.get_or_create(user=request.user)
    rooms = Chat.objects.filter(participants=profile)
    participants = ''
    for i in chat.participants.all():
        if profile != i:
            participants += ', {}'.format(i)
    if profile in chat.participants.all():
        return render(request, 'chat/room.html', {
            'room_name': mark_safe(json.dumps(room_name)),
            'username' : mark_safe(json.dumps(request.user.username)),
            'normal_room_name': room_name,
            'normal_username' : request.user.username,
            'rooms': rooms,
            'participants':participants[1:]
        })
    else:
        # TODO: message
        return redirect('chat:chat_index')



