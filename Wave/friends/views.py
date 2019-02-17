from django.http import HttpResponse
from django.core import serializers
from django.http import HttpResponseForbidden

from users.models import User
from friends.models import Follow

# Just get a list of Users on the server, minus the user making the request
def find(request):

    if not request.user.is_authenticated:
        return HttpResponseForbidden()

    server_users = User.objects.exclude(pk=request.user.id).filter(is_active=True)
    data = serializers.serialize('json', server_users, fields=('username'))
    return HttpResponse(data, content_type="application/json")


# Get a list of Users who the current user follows
def following(request):

    if not request.user.is_authenticated:
        return HttpResponseForbidden()

    # E.g., look at Follow table results where I am the follower
    following = User.objects.filter(followee__user1=request.user.id, is_active=True)
    data = serializers.serialize('json', following, fields=('username'))
    return HttpResponse(data, content_type="application/json")


# Get a list of Users who follow the current user
def followers(request):

    if not request.user.is_authenticated:
        return HttpResponseForbidden()

    # Look at Follow table results where I am the followee
    followers = User.objects.filter(follower__user2=request.user.id, is_active=True)
    data = serializers.serialize('json', followers, fields=('username'))
    return HttpResponse(data, content_type="application/json")


# Get a list of Users who the current user is friends with
def friends(request):

    if not request.user.is_authenticated:
        return HttpResponseForbidden()

    followers = User.objects.filter(follower__user2=request.user.id, is_active=True)
    following = User.objects.filter(followee__user1=request.user.id, is_active=True)
    friends = following & followers
    data = serializers.serialize('json', friends, fields=('username'))
    return HttpResponse(data, content_type="application/json")
