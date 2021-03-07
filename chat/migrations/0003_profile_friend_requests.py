# Generated by Django 3.1.7 on 2021-03-07 20:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0002_chat_profile'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='friend_requests',
            field=models.ManyToManyField(blank=True, related_name='_profile_friend_requests_+', to='chat.Profile'),
        ),
    ]
