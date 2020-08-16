from django.db import models
from django.contrib.auth import get_user_model


# Create your models here.

class Post(models.Model):
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    content = models.TextField(max_length=300)
    date_pub = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(to=get_user_model(), related_name='like')
    tags = models.CharField(max_length=100)

    class Meta:
        ordering = ['-date_pub']

    @classmethod
    def get_posts_by_user(cls, author):
        return cls.objects.filter(author=author)

    @classmethod
    def get_posts_by_tag(cls, tag):
        return cls.objects.filter(tags__contains=tag)

    @classmethod
    def get_sorted_posts(cls, order_modifier='-'):
        return cls.objects.order_by(f'{order_modifier}date_pub')

    def get_specific_post(self, post_id):
        if self.id == post_id:
            return self, Comment.objects.filter(to_post=self)

    def date_pub_timestamp(self):
        return self.date_pub.timestamp()


class Comment(models.Model):
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    content = models.TextField(max_length=300)
    to_post = models.ForeignKey(Post, on_delete=models.CASCADE)
    date_pub = models.DateTimeField(auto_now_add=True)

    def date_pub_timestamp(self):
        return self.date_pub.timestamp()
