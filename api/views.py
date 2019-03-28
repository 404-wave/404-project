from django.shortcuts import render
from django.db.models import Q

from rest_framework import pagination, generics, views, status, mixins
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.parsers import JSONParser

import socket
import requests
import uuid
import json

from users.models import User, Node, NodeSetting
from posts.models import Post
from comments.models import Comment
from friends.models import Follow, FriendRequest

from friends.views import follows

from .serializers import UserSerializer, PostSerializer, CommentSerializer, UserFriendSerializer
from .paginators import PostPagination, CommentPagination

# TODO: For privacy issues, send 403?

# TODO:
# As a server admin, I want to be able to add nodes to share with
# As a server admin, I want to be able to remove nodes and stop sharing with them.
# As a server admin, I can limit nodes connecting to me via authentication.
# As a server admin, node to node connections can be authenticated with HTTP Basic Auth
# As a server admin, I can disable the node to node interfaces for connections that are not authenticated!

# CANT POST POTS TO OTHER SERVERS???
# CAN POST COMMENTS TO OTHER SERVERS coool
# TODO: FOAF
# TODO:

def authorized(request):

    host = request.scheme + "://" + request.META['HTTP_HOST']

    # Check if the request came from a server
    # NOTE: Per Alex Wong, if a request comes from a node we are connected to,
    # then we operate on the assumption that the individual who made the request
    # on that node was, in fact, authenticated.
    nodes = Node.objects.all()
    for node in nodes:
        if host == node.host:
            return True

    node_settings = NodeSetting.objects.all()[0]
    if host == node_settings.host:
        return True
    # If the request didn't come from one of our connected nodes,
    # then check if the request came from an authenticated user
    if not request.user.is_authenticated:
        return False

    return True


# Remove all image posts from a set of posts
def filter_out_image_posts(queryset):
    new_queryset = Post.objects.none()
    for post in queryset:
        if not post.is_image:
            new_queryset |= Post.objects.filter(id=post.id)
    return new_queryset

def get_requestor_id(request):

    # Get the requestors ID, but make sure it is a valid UUID
    requestor_id = ""
    try:
        if request.GET.get('user', None) is not None:
            return uuid.UUID(request.GET['user'])
        # TODO: The request needs to have come from our server for the below
        # to be guaranteed to work
        else:
            return request.user.id
    except:
        return None

class UserAPIView(generics.GenericAPIView):

    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get(self, request, *args, **kwargs):

        if not authorized(request):
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        if 'author_id' in kwargs.keys():
            author_id = self.kwargs['author_id']
            try:
                queryset = User.objects.get(id=author_id, is_active=True)
            except:
                return Response(status=status.HTTP_404_NOT_FOUND)

        else:
            queryset = User.objects.filter(is_active=True)

        uid = author_id
        user_Q = Q()
        follow_obj = Follow.objects.filter(Q(user2=uid)|Q(user1=uid))
        
        if len(follow_obj) != 0:
            for follow in follow_obj:
                if follow.user1==uid:
                    recip_object = Follow.objects.filter(user1=follow.user2,user2=follow.user1)
                    if len(recip_object) != 0:
                        user_Q = user_Q | Q(id=follow.user2)
                elif follow.user2==uid:
                    recip_object = Follow.objects.filter(user1=follow.user2,user2=follow.user1)
                    if len(recip_object) != 0:
                        user_Q = user_Q | Q(id=follow.user1)
            if len(user_Q) != 0:
                friends = User.objects.filter(user_Q)
            else:
                friends = User.objects.none()
        else:
            friends = User.objects.none()

        serializer = UserSerializer(queryset, many=False, context={'friends':friends})
        return Response(serializer.data)


# TODO: As a server admin, I want to share or not share posts with users on other servers.
# TODO: As a server admin, I want to share or not share images with users on other servers.
class PostAPIView(generics.GenericAPIView):

    queryset = Post.objects.all()
    serializer_class = PostSerializer
    pagination_class = PostPagination

    def get(self, request, *args, **kwargs):

        if not authorized(request):
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        # Check if we have enabled sharing posts with other servers
        node_settings = None
        host = request.scheme + "://" + request.META['HTTP_HOST']

        try:
            node_settings = NodeSetting.objects.all()[0]
            if node_settings.share_posts is False:
                if not host == node_settings.host:
                    return Response(status=status.HTTP_401_UNAUTHORIZED)
        except:
            pass

        server_only = False
        if host == node_settings.host:
            server_only = True

        data = ""
        queryset = ""
        path = request.path
        requestor_id = get_requestor_id(request)

        if requestor_id is None:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        if 'author_id' in self.kwargs.keys():
            author_id = self.kwargs['author_id']
            try:
                author = User.objects.get(id=author_id)
            except:
                return Response(status=status.HTTP_404_NOT_FOUND)

            queryset = Post.objects.none()
            if requestor_id == author_id:
                queryset = Post.objects.filter(user=requestor_id, unlisted=False)
            else:
                queryset = Post.objects.filter_user_visible_posts_by_user_id(user_id=requestor_id, server_only=server_only).filter(user=author_id)
                queryset = queryset | Post.objects.filter(user=author_id, privacy=Post.PUBLIC)

        elif 'post_id' in kwargs.keys():
            post_id = self.kwargs['post_id']
            queryset = Post.objects.filter_user_visible_posts_by_user_id(user_id=requestor_id, server_only=server_only).filter(id=post_id)

        elif path == "/service/author/posts":
            # Get all posts visible to the requesting user
            queryset = Post.objects.filter_user_visible_posts_by_user_id(user_id=requestor_id, server_only=server_only)

        else:
            queryset = Post.objects.filter(privacy=Post.PUBLIC)

        if node_settings is not None and node_settings.share_imgs is False:
            if not host == node_settings.host:
                queryset = filter_out_image_posts(queryset)

        serializer = PostSerializer(queryset, many=True)
        data = serializer.data

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        return Response(data)

    def post(self, request, *args, **kwargs):

        if not authorized(request):
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        # TODO: We need to incorporate UUIDs for posts first
        return Response(status=status.HTTP_501_NOT_IMPLEMENTED)

    def put(self, request, *args, **kwargs):

        if not authorized(request):
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        # TODO: We need to incorporate UUIDs for posts first
        return Response(status=status.HTTP_501_NOT_IMPLEMENTED)


class CommentAPIView(generics.GenericAPIView):

    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    pagination_class = CommentPagination

    def get(self, request, *args, **kwargs):

        if not authorized(request):
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        requestor_id = get_requestor_id(request)
        if requestor_id is None:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        server_only = False
        node_settings = None
        host = request.scheme + "://" + request.META['HTTP_HOST']

        try:
            node_settings = NodeSetting.objects.all()[0]
            if host == node_settings.host:
                server_only = True
        except:
            pass

        if 'post_id' in self.kwargs.keys():
            post_id = self.kwargs['post_id']
            try:
                queryset = Post.objects.filter_user_visible_posts_by_user_id(user_id=requestor_id, server_only=server_only).filter(id=post_id)[0].comments
            except:
                Response(status=status.HTTP_404_NOT_FOUND)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = CommentSerializer(queryset, many=True)
        return Response(serializer.data)

    # TODO: POSTing comments
    def post(self, request, *args, **kwargs):

        if not authorized(request):
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        requestor_id = get_requestor_id(request)
        if requestor_id is None:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        server_only = False
        node_settings = None
        host = request.scheme + "://" + request.META['HTTP_HOST']

        try:
            node_settings = NodeSetting.objects.all()[0]
            if host == node_settings.host:
                server_only = True
        except:
            pass

        # Retrieves JSON data
        data = request.data
        try:
            post_id = data['post'] # TODO: This is a url, that's stupid, need to parse
            content = data['comment']['comment']
            content_type = data['comment']['contentType']
            timestamp = data['comment']['published']
            author_id = data['comment']['author']['id'].split("/")[-1]
        except:
            # If the JSON was not what we wanted, send a 400
            Response(status=status.HTTP_400_BAD_REQUEST)

        # Check that the requesting user has visibility of that post
        post = Post.objects.filter_user_visible_posts_by_user_id(user_id=requestor_id, server_only=server_only).filter(id=post_id)
        if post is None:
            response = {
	           "query": "addComment",
               "success": False,
               "message": "Comment not allowed"
            }
            return Response(response, status=status.HTTP_403_FORBIDDEN)

        # TODO: Create the actual post
        try:
            pass
        except:
            pass

        response = {
            "query": "addComment",
            "success": True,
            "message": "Comment Added"
        }
        return Response(response, status=status.HTTP_200_OK)


class FriendAPIView(generics.GenericAPIView):

    queryset = Follow.objects.all()
    serializer_class = UserFriendSerializer
    parser_classes = (JSONParser,)

    def get(self, request, *args, **kwargs):

        if not authorized(request):
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        if 'author_id' in self.kwargs.keys():
            author_id = self.kwargs['author_id']

            friends = ""
            try:
                
                #followers = User.objects.filter(follower__user2=author_id, is_active=True)
                # following = User.objects.filter(followee__user1=author_id, is_active=True)
                # friends = following & followers

                uid = author_id
                user_Q = Q()
                follow_obj = Follow.objects.filter(Q(user2=uid)|Q(user1=uid))

                if len(follow_obj) != 0:
                    for follow in follow_obj:
                        if follow.user1==uid:
                            recip_object = Follow.objects.filter(user1=follow.user2,user2=follow.user1)
                            if len(recip_object) != 0:
                                user_Q = user_Q | Q(id=follow.user2)
                        elif follow.user2==uid:
                            recip_object = Follow.objects.filter(user1=follow.user2,user2=follow.user1)
                            if len(recip_object) != 0:
                                user_Q = user_Q | Q(id=follow.user1)
                    if len(user_Q) != 0:
                        friends = User.objects.filter(user_Q)
                    else:
                        friends = User.objects.none()
                else:
                    friends = User.objects.none()
                
                
            except:
                return Response(status=status.HTTP_404_NOT_FOUND)

            friend_list = list()
            for friend in friends:
                friend_list.append(str(friend.id))

            return Response({"query": "friends", "authors": friend_list})

        if 'author_id1' in self.kwargs.keys() and 'author_id2' in self.kwargs.keys():

            author_id1 = self.kwargs['author_id1']
            author_id2 = self.kwargs['author_id2']

            #TODO Check if they actually exist in other servers
            a1_follows_a2 = follows(author_id1,author_id2)
            a2_follows_a1 = follows(author_id2,author_id1)

            if a1_follows_a2 & a2_follows_a1:
                friends = True
            else:
                friends = False

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

        if not authorized(request):
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
        # followers = User.objects.filter(follower__user2=author_id, is_active=True)
        # following = User.objects.filter(followee__user1=author_id, is_active=True)
        # friends = following & followers
        uid = author_id
        user_Q = Q()
        follow_obj = Follow.objects.filter(Q(user2=uid)|Q(user1=uid))

        if len(follow_obj) != 0:
            for follow in follow_obj:
                if follow.user1==uid:
                    recip_object = Follow.objects.filter(user1=follow.user2,user2=follow.user1)
                    if len(recip_object) != 0:
                        user_Q = user_Q | Q(id=follow.user2)
                elif follow.user2==uid:
                    recip_object = Follow.objects.filter(user1=follow.user2,user2=follow.user1)
                    if len(recip_object) != 0:
                        user_Q = user_Q | Q(id=follow.user1)
            if len(user_Q) != 0:
                friends = User.objects.filter(user_Q)
            else:
                friends = User.objects.none()
        else:
            friends = User.objects.none()

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
    parser_classes = (JSONParser,)
    

    def post(self, request, *args, **kwargs):

        if not authorized(request):
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        # Retrieves JSON data
        data = json.loads(request.body)

        
        try:
            author_id = data['author']['id'].split("/")[-1]
            friend_id = data['friend']['id'].split("/")[-1]
        except:
            # If the JSON was not what we wanted, send a 400
            Response(status=status.HTTP_400_BAD_REQUEST)

        following = User.objects.none()
        try:
            # followers = User.objects.filter(follower__user2=author_id, is_active=True)
            # following = User.objects.filter(followee__user1=author_id, is_active=True)
            # friends = following & followers

             following_user_Q = Q()
             following_obj = Follow.objects.filter(user1=author_id,is_active=True)
             print("we in here")
             print(len(following_obj))
             for fr in following_obj:
                 following_user_Q = following_user_Q | Q(id= fr.user2)
             following = User.objects.filter(following_user_Q)

        except:
            print("No follow objects. Continuing ")
            
        already_following = False
        if (len(following) != 0):
            for followee in following:
                if str(friend_id) == str(followee.id):
                    already_following = True
    
        # If user1 is already following user2, then a request must have previously been made
        if not already_following:
            try:
                user1 = author_id
                user2 = friend_id
                Follow.objects.create(user1=user1, user2=user2)

                # Query to see if the person they want to follow is already following requestor
                exists_in_table = FriendRequest.objects.filter(requestor=user2,recipient=user1)

                if (len(exists_in_table) == 0) & (follows(user2,user1) == False):
                    FriendRequest.objects.create(requestor= user1,recipient= user2)
                elif len(exists_in_table) != 0:
                    exists_in_table.delete()

            except:
                Response(status=status.HTTP_409_CONFLICT)

        return Response(status=status.HTTP_200_OK)
