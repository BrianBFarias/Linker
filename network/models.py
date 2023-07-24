from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class User(AbstractUser):
    pass

class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    followers = models.ManyToManyField(User, related_name="followers", blank=True)
    following = models.ManyToManyField(User, related_name="following", blank=True)

    def __str__(self):
        return f"{self.user}"
    
    def serialize(self, user):
        return{
            "profile_id": self.user.id,
            "num_followers": self.followers.count(),
            "num_following": self.following.count(),
            "followable": (not self.is_anonymous) and self.user != user
        }
    

class Post(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.CharField(max_length=60*200)
    likes = models.ManyToManyField(Profile, related_name="likes", blank=True)
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.creator}"
    
    def serialize(self, user):
        return{
            "id": self.id,
            "creator": self.creator.username,
            "creator_id": self.creator.id,
            "timestamp": self.timestamp.strftime("%b %d %Y, %I:%M %p"),
            "likes": self.likes.count(),
            "content": self.content,
            "editable": (self.creator == user)
        }