from django.shortcuts import render

from rest_framework import viewsets

from users.models import User
from posts.models import Post
from comments.models import Comment
from .serializers import UserSerializer, PostSerializer, CommentSerializer

# TODO: Learn accept query params
# TODO: Learn pagination

class UserViewSet(viewsets.ModelViewSet):

    queryset = User.objects.all()
    serializer_class = UserSerializer
    http_method_names = ['get']

    # How to ship a custom query set
    # def get_queryset(self):
    #     return User.objects.filter(is_active=True)


class PostViewSet(viewsets.ModelViewSet):

    queryset = Post.objects.all()
    serializer_class = PostSerializer
    http_method_names = ['get', 'post', 'put']


class CommentViewSet(viewsets.ModelViewSet):

    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    http_method_names = ['get', 'post']
