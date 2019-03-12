from django.urls import path, include

from rest_framework import routers

from .views import UserAPIView, PostAPIView, CommentAPIView, FriendAPIView

urlpatterns = [

    # Author Profiles
    path('author/<int:author_id>/', UserAPIView.as_view(), name="GETSingleAuthor"),
    #path('author/', UserAPIView.as_view(), name="GETAllAuthors"),

    # Posts
    path('author/<int:author_id>/posts', PostAPIView.as_view(), name="GETAuthorPosts"),
    path('posts/<int:post_id>/', PostAPIView.as_view(), name="GETSinglePost"),
    path('posts/', PostAPIView.as_view(), name="GETAllPosts"),

    #TODO: POST a post and PUT to a post

    # Comments
    path('posts/<int:post_id>/comments', CommentAPIView.as_view(), name="GETComments"),

    #TODO: POST to a comment

    # Friendship
    path('author/<int:author_id>/friends/', FriendAPIView.as_view(), name="GETFriends"),

    #TODO: POST a friendreqeust

]
