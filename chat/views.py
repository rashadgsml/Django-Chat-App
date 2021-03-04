from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils.safestring import mark_safe
from .models import Message
import json

def index(request):
    return render(request, 'chat/index.html')


def room(request, room_name):
    return render(request, 'chat/room2.html', {
        'room_name': mark_safe(json.dumps(room_name)),
        'username' : mark_safe(json.dumps(request.user.username)),
        'normal_room_name': room_name,
        'normal_username' : request.user.username,
    })