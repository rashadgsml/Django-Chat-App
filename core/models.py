from django.db import models
from chat.models import Profile, Message

class Notification(models.Model):
    from_profile = models.ForeignKey(Profile, related_name='notf_from_profile', on_delete=models.CASCADE, null=True)
    to_profile = models.ForeignKey(Profile, related_name='notf_to_profile', on_delete=models.CASCADE)
    message = models.ForeignKey(Message, on_delete=models.CASCADE, blank=True, null=True)
    content = models.CharField(max_length=50)
    is_read = models.BooleanField(default=False)
    
    def __str__(self):
        return self.to_profile.user.username

class Post(models.Model):
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    image = models.FileField()
    description = models.CharField(max_length=100)
    datetime = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.author.user.username

    class Meta:
        ordering = ['-datetime']