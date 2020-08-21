from rest_framework import serializers
from rest_framework.fields import CurrentUserDefault

from users.models import CustomUser
from users.serializers import UserSerializer
from .models import Post, Comment


class PostSerializer(serializers.HyperlinkedModelSerializer):
    #author = serializers.HyperlinkedRelatedField(view_name='customuser-detail', queryset=CustomUser.objects.all())
    #author = serializers.HyperlinkedRelatedField(view_name='customuser-detail', queryset=CustomUser.objects.all())
    author = UserSerializer(read_only=True)
    author_pk = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all(), source='author', write_only=True)
    """
    post_comments = serializers.HyperlinkedRelatedField(many=True, view_name='comment-detail',
                                                         required=False,
                                                        allow_null=True, read_only=True)
    """


    class Meta:
        model = Post
        fields = ['url', 'id', 'content', 'author', 'author_pk', 'date_pub_timestamp', 'post_comments', 'likes_count']

    def get_fields(self):
        fields = super(PostSerializer, self).get_fields()
        fields['post_comments'] = CommentSerializer(many=True, read_only=True)
        return fields

    def create(self, validated_data):
        return super().create(validated_data)


class CommentSerializer(serializers.HyperlinkedModelSerializer):
    author = UserSerializer(read_only=True)
    author_pk = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all(), source='author', write_only=True)

    class Meta:
        model = Comment
        fields = ['url', 'id', 'author', 'author_pk', 'content', 'date_pub_timestamp', 'to_post', 'likes_count']
