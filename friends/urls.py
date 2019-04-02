from django.urls import path, include

from . import views


urlpatterns = [
    path('friend_requests/', views.friend_requests, name='friend_requests'),
    path('following/', views.following, name='following'),
    path('followers/', views.followers, name='followers'),
    path('friends/', views.friends, name='friends'),
    path('find/', views.find, name='find_friends'),
    path('change_ModelDatabase/',views.change_ModelDatabase,name='change_ModelDatabase')
    path('getNodeList/',views.getNodeList,name='getNodeList')
]
