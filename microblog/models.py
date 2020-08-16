from django.db import models
from django.contrib.auth import get_user_model


# Create your models here.

class Post(models.Model):
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    content = models.TextField(max_length=300)
    date_pub = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(to=get_user_model())
    tags = models.CharField(max_length=100)


class Comment(models.Model):
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    content = models.TextField(max_length=300)
    to_post = models.ForeignKey(Post, on_delete=models.CASCADE)
    date_pub = models.DateTimeField(auto_now_add=True)