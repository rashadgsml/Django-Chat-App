from django.shortcuts import render, redirect, reverse
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.utils.safestring import mark_safe
from chat.models import Message, Chat, Profile, FriendRequest
from .models import Post
from .forms import PostForm
from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.dispatch import receiver 
from django.contrib.auth import get_user_model
from django.views.generic import ListView, DetailView, View
import random
import string


User = get_user_model()

@receiver(user_logged_in)
def got_online(sender, user, request, **kwargs):
    user.profile.status = 'online'
    user.profile.save()

@receiver(user_logged_out)
def got_offline(sender, user, request, **kwargs):
    user.profile.status = 'offline'
    user.profile.save()

@login_required
def index(request):
    posts = Post.objects.all()
    profile, created = Profile.objects.get_or_create(user=request.user)
    profiles = Profile.objects.all()
    sent_request_list = []
    for i in profile.friend_requests.all():
        sent_request_list.append(i.to_profile)
    context = {
        'profile': profile,
        'posts': posts,
        'profiles': profiles,
        'sent_request_list': sent_request_list,
    }
    return render(request, 'index2.html', context)

@login_required
def friends(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    profiles = Profile.objects.all()
    friend_requests = profile.friend_requests.all().filter(to_profile=profile)
    sent_request_list = []
    for i in profile.friend_requests.all():
        sent_request_list.append(i.to_profile)
    context = {
        'profile': profile,
        'profiles': profiles,
        'friend_requests': friend_requests,
        'sent_request_list': sent_request_list,
    }
    return render(request,'friends.html', context)

@login_required
def notifications(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    profiles = Profile.objects.all()
    friend_requests = profile.friend_requests.all().filter(to_profile=profile)
    sent_request_list = []
    for i in profile.friend_requests.all():
        sent_request_list.append(i.to_profile)
    context = {
        'profile': profile,
        'profiles': profiles,
        'friend_requests': friend_requests,
        'sent_request_list': sent_request_list,
    }
    return render(request,'notifications.html',context)

@login_required
def send_friend_request(request):
    user_data = request.POST.get('user')
    the_user = User.objects.get(username = user_data)

    user_profile = Profile.objects.get(user=the_user)
    my_profile = Profile.objects.get(user=request.user)

    friend_request_qs = FriendRequest.objects.filter(from_profile=my_profile,to_profile=user_profile)
    if not friend_request_qs.exists():
        friend_request = FriendRequest.objects.create(from_profile=my_profile, to_profile=user_profile)
        user_profile.friend_requests.add(friend_request)
        my_profile.friend_requests.add(friend_request)
        # TODO: friend request successfully sent
    return redirect(request.META['HTTP_REFERER'])

@login_required
def cancel_friend_request(request):
    user_data = request.POST.get('user')
    the_user = User.objects.get(username = user_data)

    user_profile = Profile.objects.get(user=the_user)
    my_profile = Profile.objects.get(user=request.user)

    FriendRequest.objects.filter(from_profile=my_profile,to_profile=user_profile).delete()
    # TODO: friend request successfully cancelled

    return redirect(request.META['HTTP_REFERER'])

@login_required
def response_friend_request(request):
    data = request.POST.get('response').split('|')
    response = data[0]
    the_user = User.objects.get(username=data[1])
    user_profile = Profile.objects.get(user=the_user)
    my_profile = Profile.objects.get(user=request.user)

    if response == 'accept':
        my_profile.friends.add(user_profile)
        # TODO: You accepted friend request
    elif response == 'decline':
        print('declined')
        # TODO: You declined the friend request
    FriendRequest.objects.filter(from_profile=user_profile, to_profile=my_profile).delete()

    return redirect(request.META['HTTP_REFERER'])

@login_required
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

@login_required
def remove_friend(request):
    friend_data = request.POST.get('friend')
    friend_user = User.objects.get(username = friend_data)
    profile, created = Profile.objects.get_or_create(user=request.user)
    friend = Profile.objects.get(user=friend_user)
    profile.friends.remove(friend)
    return redirect(request.META['HTTP_REFERER'])


class CreatePostView(View):

    def get(self, *args, **kwargs):
        form = PostForm
        context = {'form':form}
        return render(self.request,'new_post.html',context)

    def post(self, *args, **kwargs):
        form = PostForm(self.request.POST or None, self.request.FILES or None)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = Profile.objects.get(user=self.request.user)
            post.save()
            # TODO: message
            return redirect('core:index')
        return redirect('core:index')
            

