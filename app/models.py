from django.db import models
from django.contrib.auth.models import User

from dataclasses import dataclass
import datetime


class Post(models.Model):
    body = models.CharField(max_length=200)
    user = models.ForeignKey(User, related_name="posts", on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now=True)


class PostLike(models.Model):
    user = models.ForeignKey(User, related_name="liked_by", on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name="post_liked", on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "post"], name="unique_post_like"
            )
        ]

class UserFollowing(models.Model):
    user = models.ForeignKey(User, related_name='user', on_delete=models.CASCADE) # user_id of user who want to follow other user
    user_to_follow = models.ForeignKey(User, related_name='user_follower', on_delete=models.CASCADE) # user_id of user account who you want to follow
    timestamp_followed= models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "user_to_follow"], name="unique_follower"
            )
        ]
        verbose_name_plural = 'Followers'
        verbose_name = 'Follower'
        ordering = ['timestamp_followed']

@dataclass
class Feed:
    id: int
    body: str
    timestamp: datetime.datetime
    author: str
    likes: int
    
    def to_dict(p):
        if isinstance(p, Feed):
            dict = {
                "id": p.id,
                "body": p.body,
                "author": p.author,
                "likes": p.likes
            }
            return dict
        else:
            type_name = p.__class__.__name__
            raise TypeError("Unexpected type {0}".format(type_name))