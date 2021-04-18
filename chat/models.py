from django.db import models
from django.contrib.auth import get_user_model
from django.dispatch import receiver
from django.db.models.signals import post_save

User = get_user_model()

class FriendRequest(models.Model):
    from_profile = models.ForeignKey('Profile', related_name='from_profile' ,on_delete=models.CASCADE)
    to_profile = models.ForeignKey('Profile', related_name='to_profile' ,on_delete=models.CASCADE)

    def __str__(self):
        return self.from_profile.user.username

class Profile(models.Model):
    user = models.OneToOneField(User, blank=True, null=True, on_delete=models.CASCADE)
    friends = models.ManyToManyField('self', blank=True)
    friend_requests = models.ManyToManyField(FriendRequest, blank=True)
    status = models.CharField(max_length=15, default='offline')

    def __str__(self):
        return self.user.username

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    try:
        instance.profile.save()
    except:
        print("Exception")

class Message(models.Model):
    author = models.ForeignKey(User, related_name='author_messages', on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def last_10_messages():
        return Message.objects.order_by('-timestamp').all()[:10]
    
    def __str__(self):
        return self.content

class Chat(models.Model):
    room_name = models.CharField(max_length=10)
    participants = models.ManyToManyField(Profile, blank=True)
    messages = models.ManyToManyField(Message, blank=True)

    def last_10_messages(self):
        return self.messages.all().order_by('-timestamp').all()[:10]

    def delete_room():
        for i in Chat.objects.all():
            if i.participants.count() == 1:
                i.delete()

    def __str__(self):
        return self.room_name

