from django.shortcuts import render

from rest_framework import pagination, generics, views, status, mixins
from rest_framework.response import Response
from rest_framework.views import APIView

import requests

from users.models import User
from posts.models import Post
from comments.models import Comment
from friends.models import Follow, FriendRequest

from friends.views import follows

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
        path = request.path
        print(request.path)
        if 'author_id' in self.kwargs.keys():
            author_id = self.kwargs['author_id']
            try:
                author = User.objects.get(id=author_id)
            except:
                return Response(status=status.HTTP_404_NOT_FOUND)
            queryset = Post.objects.filter_user_visible_posts(user=request.user).filter(user=author_id)

            # TODO: Improve the below query -- doesn't cover entire domain. E.g., private and unlisted.
            queryset = queryset | Post.objects.filter(user=author_id, privacy=Post.PUBLIC)

        elif 'post_id' in kwargs.keys():
            post_id = self.kwargs['post_id']
            queryset = Post.objects.filter_user_visible_posts(user=request.user).filter(id=post_id)
            # if not queryset:
            #     return Response(status=status.HTTP_404_NOT_FOUND)

        elif path == "/service/author/posts":
            print("CYAYAYAY")
            queryset = Post.objects.filter_user_visible_posts(user=request.user)

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
        # TODO: We need to incorporate UUIDs for posts first
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


class FriendAPIView(generics.GenericAPIView):

    queryset = Follow.objects.all()

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

        # TODO: Authentication
        # if not request.user.is_authenticated:
        #     return Response(status=status.HTTP_401_UNAUTHORIZED)

        # Retrieves JSON data
        data = request.data
        try:
            author = data['author']
            authors = data['authors']
        except:
            # If the JSON was not what we wanted, send a 400
            Response(status=status.HTTP_400_BAD_REQUEST)

        author_id = author.split("/")[-1]
        followers = User.objects.filter(follower__user2=author_id, is_active=True)
        following = User.objects.filter(followee__user1=author_id, is_active=True)
        friends = following & followers

        friend_list = list()
        for potential_friend in authors:
            potential_friend_id = potential_friend.split("/")[-1]
            for friend in friends:
                if str(friend.id) == potential_friend_id:
                    friend_list.append(potential_friend)
                    break

        response = {
            "query":"friends",
            "author": author,
            "authors": friend_list
        }

        return Response(response)


class FriendRequestAPIView(generics.GenericAPIView):

    queryset = FriendRequest.objects.all()

    def post(self, request, *args, **kwargs):

        # TODO: Authentication
        # if not request.user.is_authenticated:
        #     return Response(status=status.HTTP_401_UNAUTHORIZED)

        # Retrieves JSON data
        data = request.data
        try:
            author_id = data['author']['id'].split("/")[-1]
            friend_id = data['friend']['id'].split("/")[-1]
        except:
            # If the JSON was not what we wanted, send a 400
            Response(status=status.HTTP_400_BAD_REQUEST)

        try:
            followers = User.objects.filter(follower__user2=author_id, is_active=True)
            following = User.objects.filter(followee__user1=author_id, is_active=True)
            friends = following & followers
        except:
            # TODO: What is the correct status code here?
            Response(status=status.HTTP_200_OK)

        already_following = False
        for followee in following:
            if str(friend_id) == str(followee.id):
                already_following = True

        # If user1 is already following user2, then a request must have previously been made
        if not already_following:
            try:
                user1 = User.objects.get(pk=author_id)
                user2 = User.objects.get(pk=friend_id)
                Follow.objects.create(user1=user1, user2=user2)

                # Query to see if the person they want to follow is already following requestor
                exists_in_table = FriendRequest.objects.filter(requestor=user2,recipient=user1)

                if (len(exists_in_table) == 0) & (follows(user2,user1) == False):
                    FriendRequest.objects.create(requestor= user1,recipient= user2)
                elif len(exists_in_table) != 0:
                    exists_in_table.delete()

            except:
                # TODO: What is the correct status code here?
                Response(status=status.HTTP_200_OK)

        return Response(status=status.HTTP_200_OK)
