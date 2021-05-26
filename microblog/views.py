from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import viewsets, status
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import NotAuthenticated
from rest_framework.fields import CurrentUserDefault
from rest_framework.response import Response
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
    IsAuthenticatedOrReadOnly,
)
from rest_framework.decorators import action

from users.models import CustomUser
from users.serializers import CustomUserSerializer
from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer


def like(request, obj):
    return_message = ""
    serializer = None
    if isinstance(obj, Post):
        return_message = "You can't like your own Post."
        serializer = PostSerializer(obj, context={"request": request})
    elif isinstance(obj, Comment):
        return_message = "You can't like your own Comment."
        serializer = CommentSerializer(obj, context={"request": request})
    if request.user.is_anonymous:
        raise NotAuthenticated
    if obj.author == request.user:
        return Response({"message": return_message}, status=status.HTTP_400_BAD_REQUEST)
    if obj.liked.filter(id=request.user.id).exists():
        obj.liked.remove(request.user)
        obj.save()
    else:
        obj.liked.add(request.user)
        obj.save()

    print(type(obj))

    return Response(serializer.data)


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [
        IsAuthenticatedOrReadOnly,
    ]

    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    # def create(self, request, *args, **kwargs):
    #     req = request.copy()
    #     print(req)
    #     print(request)
    #     req.data["author"] = CustomUserSerializer(
    #         request.user, context={"request": request}
    #     ).data["url"]
    #
    #     return super(PostViewSet, self).create(req, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(detail=True, methods=["get"])
    def like(self, request, pk=None):
        liked_post = Post.objects.get(id=pk)
        return like(request, liked_post)

    @action(detail=True, methods=["get"])
    def add_to_reading_list(self, request, pk=None):
        saved_post = Post.objects.get(id=pk)
        saved_post.to_read.add(request.user)
        return Response(
            PostSerializer(saved_post, context={"request": request}).data,
            status=status.HTTP_200_OK,
        )

    @action(detail=False, methods=["get"])
    def user_reading_list(self, request):
        posts = Post.objects.filter(to_read=request.user)
        print(posts)
        return Response(
            PostSerializer(posts, context={"request": request}, many=True).data,
            status=status.HTTP_200_OK,
        )

    @action(
        detail=False,
        methods=["delete"],
        url_path="user_reading_list/(?P<pk>\d+)",
    )
    def remove_article_to_read(self, request, pk=None):
        try:
            post_to_read = Post.objects.get(to_read=self.request.user, id=pk)
            post_to_read.to_read.remove(request.user)
            return Response(status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=["get"])
    def most_popular_tags(self, request):
        tags_by_popularity = Post.get_most_popular_tags()
        return Response(tags_by_popularity, status=status.HTTP_200_OK)

    @action(
        detail=False,
        methods=["get"],
        url_path="tag/(?P<tag>.+)",
    )
    def posts_on_tag(self, request, tag=None):
        print(tag)
        posts = Post.get_posts_by_tag(tag)
        print(posts)
        return Response(
            PostSerializer(posts, context={"request": request}, many=True).data
        )


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [
        IsAuthenticatedOrReadOnly,
    ]

    @action(detail=True, methods=["get"])
    def like(self, request, pk=None):
        liked_comment = Comment.objects.get(id=pk)
        return like(request=request, obj=liked_comment)
