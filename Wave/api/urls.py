from django.urls import path, include

from rest_framework import routers

from .views import UserAPIView, PostAPIView, CommentAPIView, FriendAPIView

urlpatterns = [

    # Author Profiles
    path('author/<uuid:author_id>/', UserAPIView.as_view(), name="GETAuthorProfile"),

    # Posts
    path('author/<uuid:author_id>/posts', PostAPIView.as_view(), name="GETAuthorPosts"),
    path('posts/<int:post_id>', PostAPIView.as_view(), name="GETSinglePost"),
    path('posts/', PostAPIView.as_view(), name="GETAllPosts"),

    #TODO: POST a post and PUT to a post

    # Comments
    path('posts/<int:post_id>/comments', CommentAPIView.as_view(), name="GETPostComments"),

    #TODO: POST to a comment

    # Friendship
    path('author/<uuid:author_id>/friends/', FriendAPIView.as_view(), name="GETFriends"),
    path('author/<uuid:author_id1>/friends/<uuid:author_id2>', FriendAPIView.as_view(), name="GETAreFriends"),


    #TODO: POST a friendreqeust

]
