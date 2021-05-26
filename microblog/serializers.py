from rest_framework import serializers
from rest_framework.fields import CurrentUserDefault

from users.models import CustomUser
from users.serializers import CustomUserSerializer
from .models import Post, Comment


class PostSerializer(serializers.HyperlinkedModelSerializer):
    author = CustomUserSerializer(read_only=True)
    # author_pk = serializers.PrimaryKeyRelatedField(
    #    queryset=CustomUser.objects.all(), source="author", write_only=True
    # )

    class Meta:
        model = Post
        fields = [
            "url",
            "id",
            "title",
            "description",
            "image",
            "content",
            "author",
            # "author_pk",
            "tags",
            "date_pub_timestamp",
            "post_comments",
            "likes_count",
        ]
        # extra_kwargs = {
        #    "tags": {"read_only": True},
        # }

    def is_liked_by_user(self, post):
        user = self.context["request"].user
        print(user)
        return post.is_liked_by_user(user)

    def get_fields(self):
        fields = super(PostSerializer, self).get_fields()
        fields["post_comments"] = CommentSerializer(many=True, read_only=True)
        fields["is_liked_by_user"] = serializers.SerializerMethodField(
            "is_liked_by_user"
        )
        return fields


class CommentSerializer(serializers.HyperlinkedModelSerializer):
    author = CustomUserSerializer(read_only=True)
    author_pk = serializers.PrimaryKeyRelatedField(
        queryset=CustomUser.objects.all(), source="author", write_only=True
    )

    class Meta:
        model = Comment
        fields = [
            "url",
            "id",
            "author",
            "author_pk",
            "content",
            "date_pub_timestamp",
            "to_post",
            "likes_count",
        ]

    def is_liked_by_user(self, comment):
        user = self.context["request"].user
        print(user)
        return comment.is_liked_by_user(user)

    def get_fields(self):
        fields = super(CommentSerializer, self).get_fields()
        fields["is_liked_by_user"] = serializers.SerializerMethodField(
            "is_liked_by_user"
        )
        return fields
