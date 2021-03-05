from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils.safestring import mark_safe
from .models import Message, Chat, Profile
import json


def index(request):
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
        return render(request, 'chat/room2.html', {
            'room_name': mark_safe(json.dumps(room_name)),
            'username' : mark_safe(json.dumps(request.user.username)),
            'normal_room_name': room_name,
            'normal_username' : request.user.username,
            'rooms': rooms,
            'participants':participants[1:]
        })
    else:
        # TODO: message
        return redirect('chat:index')


