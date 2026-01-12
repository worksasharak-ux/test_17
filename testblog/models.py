from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import *


# Create your models here.

user_model= get_user_model()

class Post(models.Model):
    post_text = TextField()
    author = models.ForeignKey(user_model, on_delete=models.CASCADE)
    post_time = DateTimeField(auto_now_add=True)