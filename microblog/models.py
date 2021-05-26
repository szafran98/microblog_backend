from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.postgres.fields import ArrayField
import regex


class Post(models.Model):
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    title = models.TextField(max_length=100)
    description = models.TextField()
    tags = ArrayField(models.CharField(max_length=20), default=list)
    image = models.URLField(null=False)
    content = models.TextField()
    date_pub = models.DateTimeField(auto_now_add=True)
    liked = models.ManyToManyField(to=get_user_model(), related_name="PostLikeToggle")
    to_read = models.ManyToManyField(to=get_user_model(), related_name="ToRead")

    class Meta:
        ordering = ["-date_pub"]

    @classmethod
    def get_posts_by_user(cls, author):
        return cls.objects.filter(author=author)

    @classmethod
    def get_posts_by_tag(cls, tag):
        return cls.objects.filter(tags__contains=[tag])

    @classmethod
    def get_sorted_posts(cls, order_modifier="-"):
        return cls.objects.order_by(f"{order_modifier}date_pub")

    @classmethod
    def get_most_popular_tags(cls):
        tags_dict = {}
        for post in cls.objects.all():
            # print(post.tags)
            for tag in post.tags:
                if tag in tags_dict:
                    tags_dict[tag] = tags_dict[tag] + 1
                    print("Jest już klucz " + tag)
                else:
                    tags_dict.update({tag: 1})
        return tags_dict

    @classmethod
    def to_read_by_user(cls, user):
        return cls.objects.filter(to_read=user)

    def get_specific_post(self, post_id):
        if self.id == post_id:
            return self, Comment.objects.filter(to_post=self)

    @property
    def post_author(self):
        return {"username": self.author.username, "email": self.author.email}

    @property
    def post_comments(self):
        return Comment.objects.filter(to_post=self)

    @property
    def date_pub_timestamp(self):
        return self.date_pub.timestamp()

    @property
    def likes_count(self):
        return self.liked.count()

    # @property
    # def tags(self):
    #    tags = []
    #    for word in self.content.split():
    #        if regex.match("[#]\w+", word):
    #            tags.append(word)
    #    return tags

    def is_liked_by_user(self, user):
        return self.liked.filter(id=user.id).exists()


class Comment(models.Model):
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    content = models.TextField(max_length=300)
    to_post = models.ForeignKey(Post, on_delete=models.CASCADE)
    date_pub = models.DateTimeField(auto_now_add=True)
    liked = models.ManyToManyField(
        to=get_user_model(), related_name="CommentLikeToggle"
    )

    @property
    def date_pub_timestamp(self):
        return self.date_pub.timestamp()

    @property
    def likes_count(self):
        return self.liked.count()

    def is_liked_by_user(self, user):
        return self.liked.filter(id=user.id).exists()
