from django.shortcuts import render
from django.http import HttpResponse
from django.core import serializers

from users.models import User, Follow


# TODO: use the REST API once it is established
# TODO: Investiagte fk relationship traversal via query sets
def home(request):

    return render(request, 'home.html')


# Just get a list of Users on the server, minus the user making the request
def find(request):

    server_users = User.objects.exclude(pk=request.user.id).filter(is_active=True)
    data = serializers.serialize('json', server_users)
    return HttpResponse(data, content_type="application/json")


# Get a list of Users who the current user follows
def following(request):

    # People that I follow
    # User.objects.filter(followee__user1=request.user.id)
    # E.g., look at Follow table results where I am the followee

    following = User.objects.filter(followee__user1=request.user.id, is_active=True)
    data = serializers.serialize('json', following)
    return HttpResponse(data, content_type="application/json")


# Get a list of users who follow the current user
def followers(request):

    # People that follow me
    # User.objects.filter(follower__user2=request.user.id)
    # E.g., look at Follow table results where I am the follower

    followers = User.objects.filter(follower__user2=request.user.id, is_active=True)
    data = serializers.serialize('json', followers)
    return HttpResponse(data, content_type="application/json")


# Get a list of Users who the current user is friends with
def friends(request):

    data = dict()
    return HttpResponse(data, content_type="application/json")
