from django.db import models
from django.contrib.auth import get_user_model


# Create your models here.

"""
class Like(models.Model):
    who_likes = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    to_post = models.ForeignKey('Post', on_delete=models.CASCADE)
"""

class Post(models.Model):
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    content = models.TextField(max_length=300)
    date_pub = models.DateTimeField(auto_now_add=True)
    liked = models.ManyToManyField(to=get_user_model(), related_name='PostLikeToggle')
    #tags = models.CharField(max_length=100, default='', null=True)

    class Meta:
        ordering = ['-date_pub']

    @classmethod
    def get_posts_by_user(cls, author):
        return cls.objects.filter(author=author)

    @classmethod
    def get_posts_by_tag(cls, tag):
        return cls.objects.filter(content__contains=tag)

    @classmethod
    def get_sorted_posts(cls, order_modifier='-'):
        return cls.objects.order_by(f'{order_modifier}date_pub')

    def get_specific_post(self, post_id):
        if self.id == post_id:
            return self, Comment.objects.filter(to_post=self)

    @property
    def post_author(self):
        return {
            'username': self.author.username,
            'email': self.author.email
        }


    @property
    def post_comments(self):
        return Comment.objects.filter(to_post=self)


    @property
    def date_pub_timestamp(self):
        return self.date_pub.timestamp()

    @property
    def likes_count(self):
        return self.liked.count()

    def is_liked_by_user(self, user):
        return self.liked.filter(id=user.id).exists()

    @property
    def tags(self):
        tags = []
        for word in self.content.split():
            if '#' in word:
                tags.append(word)
        return tags


class Comment(models.Model):
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    content = models.TextField(max_length=300)
    to_post = models.ForeignKey(Post, on_delete=models.CASCADE)
    date_pub = models.DateTimeField(auto_now_add=True)
    liked = models.ManyToManyField(to=get_user_model(), related_name='CommentLikeToggle')

    @property
    def date_pub_timestamp(self):
        return self.date_pub.timestamp()

    @property
    def likes_count(self):
        return self.liked.count()
