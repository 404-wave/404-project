from django.shortcuts import render

from rest_framework import pagination, generics, views, status, mixins
from rest_framework.response import Response

from rest_framework.views import APIView

# Investigate permissons
#from rest_framework.permissions import IsAdminUser

import requests

from users.models import User
from posts.models import Post
from comments.models import Comment
from .serializers import UserSerializer, PostSerializer, CommentSerializer
from .paginators import PostPagination, CommentPagination

# TODO: For privacy issues, send 403

class UserAPIView(generics.GenericAPIView):

    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get(self, request, *args, **kwargs):

        # if not request.user.is_authenticated:
        #     return Response(status=status.HTTP_401_UNAUTHORIZED)

        # Handle GETs for multiple author profiles, or a single profile
        if 'author_id' in kwargs.keys():
            author_id = self.kwargs['author_id']
            try:
                queryset = User.objects.get(id=author_id, is_active=True)
            except:
                return Response(status=status.HTTP_404_NOT_FOUND)

        else:
            queryset = User.objects.filter(is_active=True)

        # Find the friends of the user...
        # TODO: Refactor to get_friends(author_id)
        followers = User.objects.filter(follower__user2=author_id, is_active=True)
        following = User.objects.filter(followee__user1=author_id, is_active=True)
        friends = following & followers

        serializer = UserSerializer(queryset, many=False, context={'friends':friends})
        return Response(serializer.data)


class PostAPIView(generics.GenericAPIView):

    queryset = Post.objects.all()
    serializer_class = PostSerializer
    pagination_class = PostPagination

    def get(self, request, *args, **kwargs):


        # As a server admin, I want to share or not share posts with users on other servers.
        # As a server admin, I want to share or not share images with users on other servers.
        # TODO: Add server settings check to see if we even want to share this info

        # if not request.user.is_authenticated:
        #     return Response(status=status.HTTP_401_UNAUTHORIZED)

        # Handle GETs for all public posts, or just a single post
        data = ""
        queryset = ""
        if 'author_id' in self.kwargs.keys():
            author_id = self.kwargs['author_id']
            # TODO: Hanlde the privacy concerns of the posts w.r.t authenticated user of API
            queryset = Post.objects.filter(user=author_id)
            serializer = PostSerializer(queryset, many=True)
            data = serializer.data

        elif 'post_id' in kwargs.keys():
            post_id = self.kwargs['post_id']
            # TODO: Hanlde the privacy concerns of the posts w.r.t authenticated user of API
            queryset = Post.objects.filter(id=post_id)
            serializer = PostSerializer(queryset, many=True)
            data = serializer.data

        else:
            queryset = Post.objects.filter(privacy=Post.PUBLIC)
            serializer = PostSerializer(queryset, many=True)
            data = serializer.data
            #return Response(serializer.data)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        #serializer = PostSerializer(data, many=True)
        return Response(data)

    def post(self, request, *args, **kwargs):
        return Response(status=status.HTTP_501_NOT_IMPLEMENTED)

    def put(self, request, *args, **kwargs):
        return Response(status=status.HTTP_501_NOT_IMPLEMENTED)


class CommentAPIView(generics.GenericAPIView):

    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    pagination_class = CommentPagination

    def get(self, request, *args, **kwargs):

        # if not request.user.is_authenticated:
        #     return Response(status=status.HTTP_401_UNAUTHORIZED)

        # Handle GETs for all comments belonging to a post
        if 'post_id' in self.kwargs.keys():
            post_id = self.kwargs['post_id']
            # TODO: Hanlde the privacy concerns of the post w.r.t authenticated user of API?
            # E.g., privacy inheritance

            try:
                queryset = Post.objects.filter(id=post_id)[0].comments
            except:
                Response(status=status.HTTP_404_NOT_FOUND)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = CommentSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        return Response(status=status.HTTP_501_NOT_IMPLEMENTED)


#class FriendAPIView(generics.GenericAPIView, mixins.CreateModelMixin):
class FriendAPIView(generics.GenericAPIView):

    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    pagination_class = CommentPagination

    def get(self, request, *args, **kwargs):

        # if not request.user.is_authenticated:
        #     return Response(status=status.HTTP_401_UNAUTHORIZED)

        # GET the friends of a user
        if 'author_id' in self.kwargs.keys():
            author_id = self.kwargs['author_id']

            # Build queryset for the friends of the specified author
            friends = ""
            try:
                followers = User.objects.filter(follower__user2=author_id, is_active=True)
                following = User.objects.filter(followee__user1=author_id, is_active=True)
                friends = following & followers
            except:
                return Response(status=status.HTTP_404_NOT_FOUND)

            # Iterate over the queryset to find the IDs of the friends
            friend_list = list()
            for friend in friends:
                friend_list.append(str(friend.id))

            return Response({"query": "friends", "authors": friend_list})

        # GET to see if two users are friends
        if 'author_id1' in self.kwargs.keys() and 'author_id2' in self.kwargs.keys():

            # Build queryset for the friends of the specified author
            author_id1 = self.kwargs['author_id1']
            author_id2 = self.kwargs['author_id2']

            # Get a friend list for one of the users
            friend_list = ""
            try:
                followers = User.objects.filter(follower__user2=author_id1, is_active=True)
                following = User.objects.filter(followee__user1=author_id1, is_active=True)
                friend_list = following & followers
            except:
                return Response(status=status.HTTP_404_NOT_FOUND)

            # Iterate over the friend list to check for friendship
            friends = False
            for friend in friend_list:
                if friend.id == author_id2:
                    friends = True
                    break

            # Whether there is friendship or not, we need some author data
            author1 = User
            author2 = User
            try:
                author1 = User.objects.get(id=author_id1)
                author2 = User.objects.get(id=author_id2)
            except:
                return Response(status=status.HTTP_404_NOT_FOUND)

            # Format the response
            response = {
                "query":"friends",
                "authors":[
                    str(author1.host) + str(author1.id),
                    str(author2.host) + str(author2.id)
                ],
                "friends": friends
            }

            return Response(response)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def post(self, request, *args, **kwargs):

        data = request.data

        author_id = data['author']
        author_list = data['authors']

        r = requests.get()

        friend_list = list()

        # Parse out the host

        return Response(status=status.HTTP_501_NOT_IMPLEMENTED)
