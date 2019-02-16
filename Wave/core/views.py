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

    users = list()
    following = Follow.objects.filter(user1=request.user.id)
    for f in following.values():

        try:
            user = User.objects.get(pk=f['user2_id'], is_active=True)
        except:
            continue

        users.append(user)

    user_data = serializers.serialize('json', users)
    return HttpResponse(user_data, content_type="application/json")


# Get a list of users who follow the current user
def followers(request):

    users = list()
    followers = Follow.objects.filter(user2=request.user.id)
    for f in followers.values():

        try:
            user = User.objects.get(pk=f['user1_id'], is_active=True)
        except:
            continue

        users.append(user)

    user_data = serializers.serialize('json', users)
    return HttpResponse(user_data, content_type="application/json")


# Get a list of Users who the current user is friends with
def friends(request):

    data = dict()
    return HttpResponse(data, content_type="application/json")
