from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import *
# Create your models here.

user_model= get_user_model()

class Post(models.Model):
    post_text = TextField(blank=True)
    author = models.ForeignKey(user_model, on_delete=models.CASCADE)
    post_time = DateTimeField(auto_now_add=True)
    picture = ImageField(null=True, blank=True)

    def likes_count(self):
        return PostLike.objects.filter(post=self).count()

    def is_liked_by(self, user):
        if user.is_anonymous:
            return False
        return PostLike.objects.filter(post=self, author=user).exists()

class Comment(models.Model):
    post = ForeignKey(Post, on_delete=models.CASCADE)
    author = models.ForeignKey(user_model, on_delete=CASCADE)
    text = models.TextField(blank=True)
    created_at = DateTimeField(auto_now_add=True)
    picture = ImageField(null=True, blank=True)

    def clikes_count(self):
        return CommentLike.objects.filter(comment=self).count()

    def is_cliked_by(self, user):
        if user.is_anonymous:
            return False
        return CommentLike.objects.filter(comment=self, author=user).exists()

class Like(models.Model):
    author = models.ForeignKey(user_model, on_delete=CASCADE)

class PostLike(Like):
    post = models.ForeignKey(Post, on_delete=CASCADE)

class CommentLike(Like):
    comment = models.ForeignKey(Comment, on_delete=CASCADE)