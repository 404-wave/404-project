from django.urls import path, include

from rest_framework import routers

from .views import UserAPIView, PostAPIView, CommentAPIView
from .views import FriendAPIView, FriendRequestAPIView


urlpatterns = [
    path('author/<uuid:author_id>/', UserAPIView.as_view()),
    path('posts/<uuid:post_id>/comments/', CommentAPIView.as_view()),
    path('author/<uuid:author_id1>/friends/<str:hostname>/<uuid:author_id2>/',FriendAPIView.as_view()),
    path('author/<uuid:author_id>/friends/', FriendAPIView.as_view()),
    path('friendrequest/', FriendRequestAPIView.as_view()),
    path('author/<uuid:author_id>/posts/', PostAPIView.as_view()),
    path('posts/<uuid:post_id>/', PostAPIView.as_view()),
    path('author/posts/', PostAPIView.as_view()),
    path('posts/', PostAPIView.as_view()),
]
