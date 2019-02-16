from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('friends/find/', views.find, name='find_friends'),
    path('friends/following/', views.following, name='following'),
    path('friends/followers/', views.followers, name='followers'),
    path('friends/friends/', views.friends, name='friends'),
]
