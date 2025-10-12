# accounts/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    bio = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profiles/', blank=True, null=True)

    # Users this user follows (directional). Reverse name will be "followers".
    following = models.ManyToManyField(
        'self',
        symmetrical=False,
        related_name='followers',
        blank=True
    )

    def __str__(self):
        return self.username

    def follow(self, other_user):
        """Follow another user (no-op if already following or self)."""
        if other_user and other_user != self:
            self.following.add(other_user)

    def unfollow(self, other_user):
        """Unfollow another user (no-op if not following or self)."""
        if other_user and other_user != self:
            self.following.remove(other_user)
