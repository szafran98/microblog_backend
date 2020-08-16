from django.shortcuts import render
from django.contrib.auth import get_user_model
from rest_framework import viewsets
from rest_framework.authtoken.models import Token
from rest_framework.response import Response

from users.models import CustomUser
from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def create(self, request, *args, **kwargs):
        try:
            new_dict = request.data.copy()
            user = CustomUser.get_user_by_token(request)
            new_dict['author'] = user.id
            serializer = self.serializer_class(data=new_dict, context={'request': request})
            serializer.is_valid(raise_exception=True)
            post = serializer.validated_data
            post = Post.objects.create(**post)
            return Response({
                'author': post.author.username,
                'content': post.content,
                'date_pub': post.date_pub_timestamp,
                'likes_count': post.likes_count
            })
        except Exception:
            raise Exception


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
