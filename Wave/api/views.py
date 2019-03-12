from django.shortcuts import render

from rest_framework import pagination, generics, views, status
from rest_framework.response import Response

# Investigate permissons
#from rest_framework.permissions import IsAdminUser

from users.models import User
from posts.models import Post
from comments.models import Comment
from .serializers import UserSerializer, PostSerializer, CommentSerializer
from .paginators import UserPagination, PostPagination, CommentPagination


class UserAPIView(generics.GenericAPIView):

    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = UserPagination

    def get(self, request, *args, **kwargs):

        # Handle GETs for multiple author profiles, or a single profile
        if 'author_id' in kwargs.keys():
            author_id = self.kwargs['author_id']
            try:
                queryset = User.objects.get(id=author_id, is_active=True)
            except User.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            queryset = User.objects.filter(is_active=True)

        # TODO: Handle error?

        # NOTE: Don't think we need to paginate here, actually.
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response({'data': serializer.data, 'request': request})

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

            # Handle GETs for all public posts, or just a single post
            if 'author_id' in self.kwargs.keys():
                author_id = self.kwargs['author_id']
                # TODO: Hanlde the privacy concerns of the posts w.r.t authenticated user of API
                queryset = Post.objects.filter(user=author_id)

            elif 'post_id' in kwargs.keys():
                post_id = self.kwargs['post_id']
                # TODO: Hanlde the privacy concerns of the posts w.r.t authenticated user of API
                queryset = Post.objects.filter(id=post_id)

            else:
                queryset = Post.objects.filter(privacy=Post.PUBLIC)

            # TODO: Handle error?

            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)

            serializer = PostSerializer(queryset, many=True)
            return Response(serializer.data)


class CommentAPIView(generics.GenericAPIView):

        queryset = Comment.objects.all()
        serializer_class = CommentSerializer
        pagination_class = CommentPagination

        def get(self, request, *args, **kwargs):

            # Handle GETs for all comments belonging to a post
            if 'post_id' in self.kwargs.keys():
                post_id = self.kwargs['post_id']
                # TODO: Hanlde the privacy concerns of the post w.r.t authenticated user of API?
                # E.g., privacy inheritance

                # TODO: This may need altering -- it is not working currently due to model interaction
                queryset = Comment.objects.filter(post=post_id)

            # TODO: Handle error?

            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)

            serializer = CommentSerializer(queryset, many=True)
            return Response(serializer.data)


class FriendAPIView(generics.GenericAPIView):

        queryset = Comment.objects.all()
        serializer_class = CommentSerializer
        pagination_class = CommentPagination

        def get(self, request, *args, **kwargs):

            # Handle GETs for all comments belonging to a post
            friend_list = list()
            if 'author_id' in self.kwargs.keys():
                author_id = self.kwargs['author_id']

                # Build queryset for the friends of the specified author
                followers = User.objects.filter(follower__user2=author_id, is_active=True)
                following = User.objects.filter(followee__user1=author_id, is_active=True)
                friends = following & followers

                # Iterate over the queryset to find the IDs of the friends
                for friend in friends:
                    friend_list.append(str(friend.id))

            #else:
                # TODO: Handle error?

            return Response({"query": "friends", "authors": friend_list})
