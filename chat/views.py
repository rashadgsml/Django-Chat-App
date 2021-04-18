from django.shortcuts import render, redirect, reverse
from django.contrib.auth.decorators import login_required
from django.utils.safestring import mark_safe
from .models import Message, Chat, Profile
import json

@login_required
def chat_index(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    rooms = Chat.objects.filter(participants=profile)
    return render(request, 'chat/index2.html', {
            'username' : mark_safe(json.dumps(request.user.username)),
            'normal_username' : request.user.username,
            'rooms': rooms,
        })

@login_required
def room(request, room_name):
    Chat.delete_room()
    chat, created = Chat.objects.get_or_create(room_name=room_name)
    profile, created = Profile.objects.get_or_create(user=request.user)
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
            'participants':participants[1:],
        })
    else:
        # TODO: message
        return redirect('chat:chat_index')

