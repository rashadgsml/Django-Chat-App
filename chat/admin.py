from django.contrib import admin
from .models import Message, Chat, Profile, FriendRequest, Notification

class MessageAdmin(admin.ModelAdmin):
    list_display = ['author',
                    'content',
                    'timestamp']

admin.site.register(Message, MessageAdmin)
admin.site.register(Chat)
admin.site.register(Profile)
admin.site.register(FriendRequest)
admin.site.register(Notification)
