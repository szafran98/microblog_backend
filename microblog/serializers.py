from rest_framework import serializers
from .models import Post, Comment


class PostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        #fields = ['id', 'author', 'content', 'date_pub_timestamp', 'tags', 'likes_count']
        fields = ['id', 'content', 'author', 'post_author', 'date_pub_timestamp', 'post_comments']



class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = ['id', 'author', 'content', 'date_pub_timestamp', 'to_post']