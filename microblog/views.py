from django.shortcuts import render
from django.contrib.auth import get_user_model
from rest_framework import viewsets, status
from rest_framework.authtoken.models import Token
from rest_framework.fields import CurrentUserDefault
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from users.models import CustomUser
from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [AllowAny,]

    """
    def create(self, request, *args, **kwargs):
        #print(self.get_serializer_context()['request'].user)
        print(request.data.get('author'))
        try:



            new_dict = request.data.copy()
            #user = CustomUser.get_user_by_token(request)
            #new_dict['author'] = user.id
            serializer = self.serializer_class(data=request.data, context={'request': request})
            serializer.is_valid(raise_exception=True)
            print(serializer)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
            #serializer = self.serializer_class(data=new_dict, context={'request': request})
            #serializer.data.setdefault('author', user.id)
            #serializer.is_valid(raise_exception=True)
            #post = serializer.validated_data
            #self.perform_create(serializer)
            #super().create(request)
            #post = serializer.validated_data
            #serializer.create(**new_dict)
            #post = Post.objects.get(author=user.id)
            #post = Post.objects.create(**post)
            #return Response({}, status=status.HTTP_201_CREATED)
            #return Response({
            #    'author': post.author.username,
             #   'content': post.content,
              #  'date_pub': post.date_pub_timestamp,
               # 'likes_count': post.likes_count
            #})
        except Exception:
            raise Exception
        """

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
