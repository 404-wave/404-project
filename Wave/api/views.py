from django.shortcuts import render

from rest_framework import pagination, generics, views, status, mixins
from rest_framework.response import Response
from rest_framework.views import APIView

import requests

from users.models import User
from posts.models import Post
from comments.models import Comment
from .serializers import UserSerializer, PostSerializer, CommentSerializer
from .paginators import PostPagination, CommentPagination

# TODO: For privacy issues, send 403?
# TODO: Is everything supposed to be paginated?

class UserAPIView(generics.GenericAPIView):

    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get(self, request, *args, **kwargs):

        # if not request.user.is_authenticated:
        #     return Response(status=status.HTTP_401_UNAUTHORIZED)

        if 'author_id' in kwargs.keys():
            author_id = self.kwargs['author_id']
            try:
                queryset = User.objects.get(id=author_id, is_active=True)
            except:
                return Response(status=status.HTTP_404_NOT_FOUND)

        else:
            queryset = User.objects.filter(is_active=True)

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

        # TODO: Only allow if 1.) user is authenticated or 2.) request came from
        # one of the nodes in our node list. This adds authentication for users
        # and will also ensure servers we have not approved cannot use the API!

        # if not request.user.is_authenticated:
        #     return Response(status=status.HTTP_401_UNAUTHORIZED)

        data = ""
        queryset = ""

        if 'author_id' in self.kwargs.keys():
            author_id = self.kwargs['author_id']
            queryset = Post.objects.filter_user_visible_posts(user=request.user).filter(user=author_id)
            serializer = PostSerializer(queryset, many=True)
            data = serializer.data

        elif 'post_id' in kwargs.keys():
            post_id = self.kwargs['post_id']
            queryset = Post.objects.filter_user_visible_posts(user=request.user).filter(id=post_id)
            serializer = PostSerializer(queryset, many=True)
            data = serializer.data

        else:
            queryset = Post.objects.filter(privacy=Post.PUBLIC)
            serializer = PostSerializer(queryset, many=True)
            data = serializer.data

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        return Response(data)

    def post(self, request, *args, **kwargs):

        # TODO: We need to incorporate UUIDs for posts first
        return Response(status=status.HTTP_501_NOT_IMPLEMENTED)

    def put(self, request, *args, **kwargs):
        return Response(status=status.HTTP_501_NOT_IMPLEMENTED)


class CommentAPIView(generics.GenericAPIView):

    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    pagination_class = CommentPagination

    def get(self, request, *args, **kwargs):

        # TODO: Only allow if 1.) user is authenticated or 2.) request came from
        # one of the nodes in our node list. This adds authentication for users
        # and will also ensure servers we have not approved cannot use the API!

        # if not request.user.is_authenticated:
        #     return Response(status=status.HTTP_401_UNAUTHORIZED)

        # Handle GETs for all comments belonging to a post
        if 'post_id' in self.kwargs.keys():
            post_id = self.kwargs['post_id']
            try:
                queryset = Post.objects.filter_user_visible_posts(user=request.user).filter(id=post_id)[0].comments
            except:
                Response(status=status.HTTP_404_NOT_FOUND)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = CommentSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):

        # TODO: We need to incorporate UUIDs for comments first
        return Response(status=status.HTTP_501_NOT_IMPLEMENTED)


#class FriendAPIView(generics.GenericAPIView, mixins.CreateModelMixin):
class FriendAPIView(generics.GenericAPIView):

    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    pagination_class = CommentPagination

    def get(self, request, *args, **kwargs):

        # TODO: Only allow if 1.) user is authenticated or 2.) request came from
        # one of the nodes in our node list. This adds authentication for users
        # and will also ensure servers we have not approved cannot use the API!

        # if not request.user.is_authenticated:
        #     return Response(status=status.HTTP_401_UNAUTHORIZED)

        if 'author_id' in self.kwargs.keys():
            author_id = self.kwargs['author_id']

            friends = ""
            try:
                followers = User.objects.filter(follower__user2=author_id, is_active=True)
                following = User.objects.filter(followee__user1=author_id, is_active=True)
                friends = following & followers
            except:
                return Response(status=status.HTTP_404_NOT_FOUND)

            friend_list = list()
            for friend in friends:
                friend_list.append(str(friend.id))

            return Response({"query": "friends", "authors": friend_list})

        # GET to see if two users are friends
        if 'author_id1' in self.kwargs.keys() and 'author_id2' in self.kwargs.keys():

            author_id1 = self.kwargs['author_id1']
            author_id2 = self.kwargs['author_id2']

            friend_list = ""
            try:
                followers = User.objects.filter(follower__user2=author_id1, is_active=True)
                following = User.objects.filter(followee__user1=author_id1, is_active=True)
                friend_list = following & followers
            except:
                return Response(status=status.HTTP_404_NOT_FOUND)

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

        print(data)
        # author_id = data['author']
        # author_list = data['authors']

        # r = requests.get()
        #
        # friend_list = list()

        # Parse out the host

        return Response(status=status.HTTP_501_NOT_IMPLEMENTED)
