from django.urls import path, include

from rest_framework import routers

from .views import UserAPIView, PostAPIView, CommentAPIView, FriendAPIView, FriendRequestAPIView

urlpatterns = [

    # Author Profiles
    path('author/<uuid:author_id>/', UserAPIView.as_view()),

    # Posts
    path('author/posts', PostAPIView.as_view()),
    path('author/<uuid:author_id>/posts', PostAPIView.as_view()),
    path('posts/<int:post_id>/', PostAPIView.as_view()),
    path('posts/', PostAPIView.as_view()),
    #TODO: POST a post and PUT to a post

    # Comments
    path('posts/<int:post_id>/comments', CommentAPIView.as_view()),
    #TODO: POST to a comment

    # Friendship
    path('author/<uuid:author_id>/friends/', FriendAPIView.as_view()),
    path('author/<uuid:author_id1>/friends/<uuid:author_id2>', FriendAPIView.as_view()),
    path('friendrequest/', FriendRequestAPIView.as_view())
]
