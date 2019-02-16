from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('friends/find/', views.find, name='find_friends'),
]
