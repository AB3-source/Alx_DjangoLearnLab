# accounts/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    bio = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)

    # 'followers' = users who follow this user.
    # related_name='following' allows user.following.all() => users this user follows.
    followers = models.ManyToManyField(
        'self', symmetrical=False, related_name='following', blank=True
    )

    def __str__(self):
        return self.username
