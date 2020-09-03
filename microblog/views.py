from django.shortcuts import render
from django.contrib.auth import get_user_model
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
from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer


def like(request, obj):
    return_message = ""
    if isinstance(obj, Post):
        return_message = "You can't like your own Post."
    elif isinstance(obj, Comment):
        return_message = "You can't like your own Comment."
    if request.user.is_anonymous:
        raise NotAuthenticated
    if obj.author == request.user:
        return Response({"message": return_message})
    if obj.liked.filter(id=request.user.id).exists():
        obj.liked.remove(request.user)
        obj.save()
    else:
        obj.liked.add(request.user)
        obj.save()

    serializer = obj.get_serializer(obj)
    return Response(serializer.data)


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [
        IsAuthenticatedOrReadOnly,
    ]

    @action(detail=True, methods=["get"])
    def like_post(self, request, pk=None):
        liked_post = Post.objects.get(id=pk)
        return like(request, liked_post)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [
        IsAuthenticatedOrReadOnly,
    ]

    @action(detail=True, methods=["get"])
    def like_comment(self, request, pk=None):
        liked_comment = Comment.objects.get(id=pk)
        return like(request=request, obj=liked_comment)
