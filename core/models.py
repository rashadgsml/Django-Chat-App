from django.db import models
from chat.models import Profile, Message

class Notification(models.Model):
    to_profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    message = models.ForeignKey(Message, on_delete=models.CASCADE)
    is_read = models.BooleanField(default=False)

class Post(models.Model):
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    image = models.FileField()
    description = models.CharField(max_length=100)
    datetime = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.author.user.username

    class Meta:
        ordering = ['-datetime']