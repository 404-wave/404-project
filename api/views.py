from django.shortcuts import render, get_object_or_404
from django.db.models import Q

from rest_framework import pagination, generics, views, status, mixins
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import UserSerializer, PostSerializer, CommentSerializer, UserFriendSerializer
from .serializers import UserFriendSerializer

from .paginators import PostPagination, CommentPagination

from friends.models import Follow, FriendRequest
from users.models import User, Node, NodeSetting
from comments.models import Comment
from posts.models import Post

from friends.views import follows

import requests
import socket
import uuid


# Checks if we have enabled sharing posts with other servers

# When you add a remote host as a user, you need to make sure to add the HOST
# field. That way we know what the hostname is of the remote host. We need this
# because some groups might not even send the remote host header, and so we
# wouldn't know who they are.
def get_hostname(request):

    users = User.objects.filter(username=request.user.username)
    if users is None:
        return None

    return users[0].host


def sharing_posts_enabled(request):

    node_settings = None
    host = get_hostname(request)
    if host is None:
        return False

    try:
        node_settings = NodeSetting.objects.all()[0]
        if node_settings.share_posts is False:
            if not host == node_settings.host:
                print("Requesting host: " + host)
                print("Requesting host: " + node_settings.host)
                return False
    except:
        pass

    return True

# TODO: Verify
def allow_server_only_posts(request):

    node_settings = None
    host = get_hostname(request)

    try:
        node_settings = NodeSetting.objects.all()[0]
    except:
        return False

    if host == node_settings.host:
        return True

    return False


def get_requestor_id(request):

    try:
        requestor_id = request.META['HTTP_X_UUID']
        return str(requestor_id)
    except:
        pass

    try:
        if request.GET.get('user', None) is not None:
            return uuid.UUID(request.GET['user'])
    except:
        return None

    return None


class UserAPIView(generics.GenericAPIView):

    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get(self, request, *args, **kwargs):

        if not request.user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

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

        data = None
        queryset = None
        path = request.path
        requestor_id = get_requestor_id(request)

        path_all_public_posts = ['/service/posts/', '/api/posts/', '/posts/']
        path_all_user_visible_posts =['/service/author/posts/',
            '/api/author/posts/', '/author/posts/']

        if not request.user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        host = get_hostname(request)
        if host is None:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        if not sharing_posts_enabled(request):
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        if requestor_id is None and path not in path_all_public_posts:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        server_only = allow_server_only_posts(request)

        # Get all posts from a single author that are visible to the requestor
        if 'author_id' in self.kwargs.keys():
            author_id = self.kwargs['author_id']
            try: author = User.objects.get(id=author_id)
            except: return Response(status=status.HTTP_404_NOT_FOUND)
            queryset = self.get_posts_from_single_author(
                author_id, requestor_id, server_only).filter(unlisted=False)

        # Get a single post if it is visible to the requesting user
        elif 'post_id' in kwargs.keys():
            post_id = self.kwargs['post_id']
            queryset = Post.objects.filter_user_visible_posts_by_user_id(
                user_id=requestor_id, server_only=server_only).filter(id=post_id)
            queryset = self.filter_out_image_posts(request, queryset)

        # Get all posts visible to the requesting user
        elif path in path_all_user_visible_posts:
            queryset = Post.objects.filter_user_visible_posts_by_user_id(
                user_id=requestor_id, server_only=server_only).filter(unlisted=False)

        # Get all public posts
        elif path in path_all_public_posts:
            queryset = Post.objects.filter(privacy=Post.PUBLIC).filter(unlisted=False).order_by('timestamp')


        # Not a valid path
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(page, many=True, context={'requestor': str(requestor_id)})
        return self.get_paginated_response(serializer.data)


    def post(self, request, *args, **kwargs):

        if not request.user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        return Response(status=status.HTTP_501_NOT_IMPLEMENTED)


    def put(self, request, *args, **kwargs):

        if not request.user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        return Response(status=status.HTTP_501_NOT_IMPLEMENTED)


    def get_posts_from_single_author(self, author_id, requestor_id, server_only):

        queryset = Post.objects.none()
        if requestor_id == author_id:
            queryset = Post.objects.filter(user=requestor_id, unlisted=False)
        else:
            queryset = Post.objects.filter_user_visible_posts_by_user_id(
                user_id=requestor_id, server_only=server_only).filter(user=author_id, unlisted=False)
            queryset = queryset | Post.objects.filter(
                user=author_id, privacy=Post.PUBLIC)

        return queryset

    # Remove all image posts from a set of posts, only if we are not sharing
    # with the server that made the request. However, if we are the server that
    # made the request, then we won't filter them out.
    def filter_out_image_posts(self, request, queryset):

        try:
            host = get_hostname(request)
            node_settings = NodeSetting.objects.all()[0]
            if node_settings.share_imgs is False:
                if not host == node_settings.host:
                    new_queryset = Post.objects.none()
                    for post in queryset:
                        if not post.is_image:
                            new_queryset |= Post.objects.filter(id=post.id)
                    return new_queryset
        except:
            pass

        return queryset


class CommentAPIView(generics.GenericAPIView):

    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    pagination_class = CommentPagination

    def get(self, request, *args, **kwargs):

        if not request.user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        requestor_id = get_requestor_id(request)
        if requestor_id is None:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        host = get_hostname(request)
        if host is None:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        server_only = allow_server_only_posts(request)

        if 'post_id' in self.kwargs.keys():
            post_id = self.kwargs['post_id']
            try:
                queryset = Post.objects.filter_user_visible_posts_by_user_id(
                    user_id=requestor_id, server_only=server_only).filter(id=post_id)[0].comments
            except:
                Response(status=status.HTTP_404_NOT_FOUND)

        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)


    def post(self, request, *args, **kwargs):

        response_failed = {
           "query": "addComment",
           "success": False,
           "message": "Comment not allowed"
        }

        response_ok = {
            "query": "addComment",
            "success": True,
            "message": "Comment Added"
        }

        if not request.user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        requestor_id = get_requestor_id(request)
        if requestor_id is None:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        server_only = allow_server_only_posts(request)

        try:
            data = request.data
            post_id = kwargs['post_id']
            content = data['comment']['comment']
            content_type = "text/plain"
            author_id = data['comment']['author']['id'].split("/")[-1]
        except:
            Response(status=status.HTTP_400_BAD_REQUEST)

        # Check that the requesting user has visibility of that post
        post = Post.objects.filter_user_visible_posts_by_user_id(
            user_id=requestor_id, server_only=server_only).filter(id=post_id)
        if post is None:
            return Response(response_failed, status=status.HTTP_403_FORBIDDEN)

        try:
            post=post[0]
            instance = get_object_or_404(Post, id=post.id)
            comment = Comment(parent=None, user=author_id, content=content, object_id=post.id, content_type=post.get_content_type)
            comment.save()
        except Exception as e:
            print(e)

        return Response(response_ok, status=status.HTTP_200_OK)


class FriendAPIView(generics.GenericAPIView):

    queryset = Follow.objects.all()
    serializer_class = UserFriendSerializer

    def get(self, request, *args, **kwargs):

        if not request.user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

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
                followers = User.objects.filter(
                    follower__user2=author_id1, is_active=True)
                following = User.objects.filter(
                    followee__user1=author_id1, is_active=True)
                friend_list = following & followers
            except:
                return Response(status=status.HTTP_404_NOT_FOUND)

            friends = False
            for friend in friend_list:
                if friend.id == author_id2:
                    friends = True
                    break

            # Whether there is friendship or not, we need some author data
            # TODO: What if one of the author's is on a different server? Then
            # we would need to make a GET request for some data to other nodes.
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

        if not request.user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

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
    serializer_class = UserFriendSerializer

    def post(self, request, *args, **kwargs):

        if not request.user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

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
                Response(status=status.HTTP_200_OK)

        return Response(status=status.HTTP_200_OK)
