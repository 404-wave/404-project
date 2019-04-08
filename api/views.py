from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from django.utils import timezone

from rest_framework import pagination, generics, views, status, mixins
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.parsers import JSONParser

import socket
import requests
import uuid
import re
import json
from .serializers import UserSerializer, PostSerializer, CommentSerializer, UserFriendSerializer

from .paginators import PostPagination, CommentPagination

from friends.models import Follow, FriendRequest,FollowManager
from users.models import User, Node, NodeSetting
from comments.models import Comment
from posts.models import Post

from friends.views import follows, standardize_url, get_user, friends

from requests.auth import HTTPBasicAuth
import requests
import socket
import uuid
import traceback


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

    # TODO: Need to check the host against the USERS host... user might be a node...

    node_settings = None
    host = get_hostname(request)
    if host is None:
        return False

    try:
        node_settings = NodeSetting.objects.all()[0]
        if node_settings.share_posts is False:
            print("Requesting host: " + host)
            print("Requesting host: " + node_settings.host)
            if not host == node_settings.host:
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

    if str(host) == str(node_settings.host):
        return True

    return False


def get_requestor_id(request):

    try:
        print ("trying X_UUID")
        requestor_id = request.META['HTTP_X_UUID']
        return str(requestor_id)
    except:
        try:
            print ("X-Request-User-ID")
            requestor_id = request.META['X-Request-User-ID']
            return str(requestor_id)
        except:
            print("When trying to resolve requestor ID, X-UUID header was not found.")
            pass

    try:
        if request.GET.get('user', None) is not None:
            return uuid.UUID(request.GET['user'])
    except:
        print("When trying to resolve requestor the 'user' query parameter was not found.")
        return None

    return None


class UserAPIView(generics.GenericAPIView):

    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get(self, request, *args, **kwargs):
        if 'author_id' in kwargs.keys():
            author_id = self.kwargs['author_id']
            try:
                queryset = User.objects.get(id=author_id, is_active=True)
            except:
                return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            queryset = User.objects.filter(is_active=True)

        # uid = author_id
        # user_Q = Q()
        # follow_obj = Follow.objects.filter(Q(user2=uid)|Q(user1=uid))
        #
        # if len(follow_obj) != 0:
        #     for follow in follow_obj:
        #         if follow.user1==uid:
        #             recip_object = Follow.objects.filter(user1=follow.user2,user2=follow.user1)
        #             if len(recip_object) != 0:
        #                 user_Q = user_Q | Q(id=follow.user2)
        #         elif follow.user2==uid:
        #             recip_object = Follow.objects.filter(user1=follow.user2,user2=follow.user1)
        #             if len(recip_object) != 0:
        #                 user_Q = user_Q | Q(id=follow.user1)
        #     if len(user_Q) != 0:
        #         friends = User.objects.filter(user_Q)
        #     else:
        #         friends = User.objects.none()
        # else:
        #     friends = User.objects.none()

        #foreign_friends = list()

        friends = get_friends_list(author_id)

        serializer = UserSerializer(queryset, many=False, context={'friends':friends, 'request':request})
        return Response(serializer.data)


    def get_friends_list(self, uid):

        # Find all people that the user follow
        following = Follow.objects.filter(user1=uid)

        # For everyone that the user follows, see who follows them back
        friends = list()
        for follow in following:
            if Follow.objects.filter(user1=follow.user2, user2=uid) is not None:
                friends.append(follow.user2)

        print("A list of the users friends...")
        print(friends)
        return friends


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

        print ("User Authenticated", request.user.is_authenticated)
        if not request.user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        print ("host", request.user.is_authenticated)
        host = get_hostname(request)
        print ("host", request.user.is_authenticated, host)
        if host is None:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        if not sharing_posts_enabled(request):
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        if requestor_id is None:
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
            try: Post.objects.get(id=post_id)
            except: return Response(status=status.HTTP_404_NOT_FOUND)
            queryset = Post.objects.filter_user_visible_posts_by_user_id(
                user_id=requestor_id, server_only=server_only).filter(id=post_id)

            if queryset.count() == 0:
                return Response(status=status.HTTP_403_FORBIDDEN)

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
        serializer = self.get_serializer(page, many=True, context={'requestor': str(requestor_id), 'request':request})

        ########################################################################
        serialized_data = serializer.data
        if path in path_all_user_visible_posts:
            for node in Node.objects.all():
                url = node.host + "/author/posts/"

                try:
                    headers = {
                        'Accept':'application/json',
                        'X-UUID': str(requestor_id)
                    }

                    response = requests.get(url, headers=headers,
                        auth=HTTPBasicAuth(str(node.username), str(node.password)))

                    print("Getting public posts from other servers...")
                    print(response.status_code)
                    if (response.status_code > 199 and response.status_code <300):
                        responselist = response.json()
                        serialized_data.extend(responselist["posts"])

                except Exception as e:
                    print("When GETting posts from other server, the following exception occured...")
                    print(e)
                    pass
        ########################################################################

        serialized_data = self.filter_out_images(request, serialized_data)
        return self.get_paginated_response(serialized_data)


    # Since we only host posts made from our server, POSTing a post requires
    # that the author is also a user on our server, otherwise a 404 will be
    # thrown. Since the accessible_users is a ManyToManyField that relies on
    # our user table, this means only users from our server can see PRIVATE
    # posts when they are first made here. If someone supplies an ID for a user
    # that can see the private post but that user isn't on our server, we will
    # just ignore it.
    def post(self, request, *args, **kwargs):

        if not request.user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        try:
            data = request.data
            author_id = uuid.UUID(data['author']['id'].split("/")[-1])
            privacy = self.resolve_privacy(data['visibility'])
            visible_to = data['visibleTo']
            unlisted = data['unlisted']
            content_type = "text/plain"
            content = data['content']
            if privacy is None:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(e)
            return Response(status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(id=author_id)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)

        try:
            post = Post(user=user, content=content, publish=timezone.now(),
                privacy=privacy, unlisted=unlisted)

            post.save()

            # Only set visible users to those on our server
            if privacy == Post.PRIVATE:
                post.accessible_users = visible_to

        except Exception as e:
            print(e)
            return Response(status=status.HTTP_503_SERVICE_UNAVAILABLE)

        return Response(status=status.HTTP_200_OK)


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
                    print("Requesting host: " + str(host))
                    print("Our host: " + str(node_settings.host))
                    new_queryset = Post.objects.none()
                    for post in queryset:
                        if not post.is_image:
                            new_queryset |= Post.objects.filter(id=post.id)
                    return new_queryset
        except:
            pass

        return queryset

    def filter_out_images(self, request, serialized_data):

        new_data = list()
        host = get_hostname(request)
        node_settings = NodeSetting.objects.all()[0]
        if node_settings.share_imgs is False:
            if not host == node_settings.host:
                for post in serialized_data:
                    if post['contentType'] == 'text/plain' or post['contentType'] == 'text/markdown':
                        new_data.append(post)
            else:
                return serialized_data
        else:
            return serialized_data

        return new_data

    def resolve_privacy(self, privacy_str):
        if privacy_str == "PUBLIC":
            return Post.PUBLIC
        elif privacy_str == "PRIVATE":
            return Post.PRIVATE
        elif privacy_str == "FRIENDS":
            return Post.FRIENDS
        elif privacy_str == "FOAF":
            return Post.FOAF
        elif privacy_str == "SERVERONLY":
            return Post.ONLY_SERVER
        else:
            return None


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

            try: Post.objects.get(id=post_id)
            except: return Response(status=status.HTTP_404_NOT_FOUND)

            try:
                queryset = Post.objects.filter_user_visible_posts_by_user_id(
                    user_id=requestor_id, server_only=server_only).filter(id=post_id)[0].comments
            except:
                Response(status=status.HTTP_404_NOT_FOUND)

        else:
            print("When GETing comments, the post ID was not found in the URL.")
            return Response(status=status.HTTP_400_BAD_REQUEST)

        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(page, many=True, context={'request':request})
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
        #
        # requestor_id = get_requestor_id(request)
        # if requestor_id is None:
        #     print("When POSTing a comment, requestor ID was not valid or was not sent.")
        #     return Response(status=status.HTTP_400_BAD_REQUEST)

        server_only = allow_server_only_posts(request)
        id_regex = '(.*)([0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12})'
        try:
            data = request.data
            re_result = re.search(id_regex, data['post'])
            post_id = uuid.UUID(re_result.group(2))
            re_result = re.search(id_regex, data['comment']['author']['id'])
            author_id = uuid.UUID(re_result.group(2))
            content = data['comment']['comment']
        except Exception as e:
            print("When POSTing a comment, there was an error parsing JSON data.")
            print(e)
            Response(status=status.HTTP_400_BAD_REQUEST)

        # Check that the requesting user has visibility of that post
        # posts = Post.objects.filter_user_visible_posts_by_user_id(
        #     user_id=requestor_id, server_only=server_only).filter(id=post_id)
        posts = Post.objects.filter_user_visible_posts_by_user_id(
            user_id=author_id, server_only=server_only).filter(id=post_id)
        if posts is None:
            print("When POSTing a comment, the requesting user did not have visibility if the post.")
            return Response(response_failed, status=status.HTTP_403_FORBIDDEN)

        try:
            post=posts[0]
            instance = get_object_or_404(Post, id=post.id)
            comment = Comment(parent=None, user=author_id, content=content, object_id=post.id, content_type=post.get_content_type)
            comment.save()
        except Exception as e:
            print("When POSTing a comment, there was an error creating the comment.")
            return Response(response_failed, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(response_ok, status=status.HTTP_200_OK)


class FriendAPIView(generics.GenericAPIView):

    queryset = Follow.objects.all()
    serializer_class = UserFriendSerializer
    parser_classes = (JSONParser,)

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)


        if 'author_id' in self.kwargs.keys():
            author_id = self.kwargs['author_id']

            friends = ""
            try:

                #followers = User.objects.filter(follower__user2=author_id, is_active=True)
                # following = User.objects.filter(followee__user1=author_id, is_active=True)
                # friends = following & followers

                uid = author_id
                follow_obj = Follow.objects.filter(Q(user2=uid)|Q(user1=uid))
                friends= set()

                if follow_obj:
                    for follow in follow_obj:
                        if ((follow.user1==uid) & (follow.user2 not in friends)):
                            recip_object = Follow.objects.filter(user1=follow.user2,user2=follow.user1)
                            if recip_object:
                                user = User.objects.filter(id=follow.user2)
                                if user:
                                    user=user.get()
                                else:
                                    user = get_user(follow.user2_server,follow.user2)
                                    if user is None:
                                        continue
                                friends.add(user)
                        elif ((follow.user2==uid) & (follow.user1 not in friends)):
                            recip_object = Follow.objects.filter(user1=follow.user2,user2=follow.user1)
                            if recip_object:
                                user= User.objects.filter(id=follow.user1)
                                if user:
                                    user=user.get()
                                else:
                                    user= get_user(follow.user1_server,follow.user1)
                                friends.add(user)


            except:

                traceback.print_exc()

                return Response(status=status.HTTP_404_NOT_FOUND)

            friend_list = list()
            for friend in friends:
                url = standardize_url(friend.host) + "service/author/"+str(friend.id)
                friend_list.append(url)



            return Response({"query": "friends", "authors": friend_list})

        if 'author_id1' in self.kwargs.keys() and 'author_id2' in self.kwargs.keys():

            author_id1 = None
            author_id2 = None
            author1_server = NodeSetting.objects.all().get()
            author1_server = standardize_url(author1_server.host)
            author2_server = None
            try:
                author_id1 = self.kwargs['author_id1']
                author_id2 = self.kwargs['author_id2']
                author2_server= self.kwargs['hostname']
                author2_server = standardize_url(author2_server)

            except:
                return Response(status=status.HTTP_400_BAD_REQUEST)

            a1_follows_a2 = follows(author_id1,author_id2)
            a2_follows_a1 = follows(author_id2,author_id1)

            if a1_follows_a2 & a2_follows_a1:
                friends = True
            else:
                friends = False
            response = {
                "query":"friends",
                "authors":[
                    author1_server +"author/"+ str(author_id1),
                    author2_server +"author/"+ str(author_id2)
                ],
                "friends": friends
            }
            return Response(response)
        else:
            print("URI doesn't exist")
            return Response(status=status.HTTP_404_NOT_FOUND)

    def post(self, request, *args, **kwargs):

        if not request.user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        # Retrieves JSON data
        data = request.data
        manager = FollowManager()

        author_id = None
        author = None
        authors = None

        try:
            author = data['author']
            author_id = author.split('/')[-1]
            authorObj = User.objects.filter(id=author_id)
            if(len(authorObj) == 0):
                return Response(status=status.HTTP_404_NOT_FOUND)
            authors = data['authors']
        except:
            # If the JSON was not what we wanted, send a 400
            return Response(status=status.HTTP_400_BAD_REQUEST)

        # followers = User.objects.filter(follower__user2=author_id, is_active=True)
        # following = User.objects.filter(followee__user1=author_id, is_active=True)
        # friends = following & followers
        friends = manager.get_friends_id(author_id)
        print(friends)

        friend_list = list()
        for potential_friend in authors:
            potential_friend_id = potential_friend.split("/")[-1]
            for friend in friends:
                if str(friend.id) == str(potential_friend_id):
                    friend_url = standardize_url(friend.host) + "service/author/"+str(friend.id)
                    friend_list.append(friend_url)
                    break

        response = {
            "query":"friends",
            "author": author,
            "authors": friend_list
        }

        return Response(response,status=status.HTTP_200_OK)


class FriendRequestAPIView(generics.GenericAPIView):

    queryset = FriendRequest.objects.all()
    serializer_class = UserFriendSerializer
    parser_classes = (JSONParser,)


    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        # Retrieves JSON data
        data = request.data

        author_id = None
        friend_id = None
        author_host = None
        friend_host = None

        try:
            author_id = data['author']['id'].split("/")[-1]
            friend_id = data['friend']['id'].split("/")[-1]
            author_host = data['author']['host']
            friend_host = data['friend']['host']

        except:
            # If the JSON was not what we wanted, send a 400
            return Response(status=status.HTTP_400_BAD_REQUEST)

        following = User.objects.none()
        print(author_id)
        print(friend_id)
        print(author_host)
        print(friend_host)

        try:
            # followers = User.objects.filter(follower__user2=author_id, is_active=True)
            # following = User.objects.filter(followee__user1=author_id, is_active=True)
            # friends = following & followers

             following_user_Q = Q()
             following_obj = Follow.objects.filter(user1=author_id,is_active=True)

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
                Follow.objects.create(user1=author_id, user1_server =author_host, user2=friend_id, user2_server = friend_host)
            except:
                print(" Couldn't create object")
                return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            print("Created object")

            # Query to see if the person they want to follow is already following requestor
            exists_in_table = FriendRequest.objects.filter(requestor=friend_id,recipient=author_id)
            if (len(exists_in_table) == 0) & (follows(friend_id,author_id) == False):
                try:
                    print("Trying to make FR")
                    FriendRequest.objects.create(requestor= author_id, requestor_server = author_host, recipient= friend_id, recipient_server = friend_host)
                except:
                    print("Couldn't make FR")
                    return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            elif len(exists_in_table) != 0:
                exists_in_table.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)
