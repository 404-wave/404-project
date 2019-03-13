from django.http import HttpResponse
from django.core import serializers
from django.http import HttpResponseForbidden
from django.shortcuts import render
from django.db.models import Q
import json

from users.models import User
from friends.models import Follow, FriendRequest
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
    print("FOLLOWERS: ", followers)
    data = serializers.serialize('json', followers, fields=('username'))
    return HttpResponse(data, content_type="application/json")

# Get a list of Users who the current user is friends with
def friends(request):

    if not request.user.is_authenticated:
        return HttpResponseForbidden()

    followers = User.objects.filter(follower__user2=request.user.id, is_active=True)
    following = User.objects.filter(followee__user1=request.user.id, is_active=True)
    friends = following & followers
    print("FRIENDS",friends)
    data = serializers.serialize('json', friends, fields=('username'))
    return HttpResponse(data, content_type="application/json") 

def follow(request):

    if not request.user.is_authenticated:
        return HttpResponseForbidden()

    followerID = request.GET['followerID']
    followeeID = request.GET['followeeID']

    # TODO: Find a good way to error handle these two DB calls
    user1 = User.objects.get(pk=followerID)
    user2 = User.objects.get(pk=followeeID)
    Follow.objects.create(user1=user1, user2=user2)

     ####add into FriendRequest table####
    #Query to see if the person they want to follow is already following requestor
    exists_in_table = FriendRequest.objects.filter(requestor=user2,recipient=user1)

    #if the other person is not following the requestor, add to table so it notifies the recipient
    if (len(exists_in_table) == 0) & (follows(user2,user1) == False):
        #print("It doesn't exist in table. Adding to table.")
        FriendRequest.objects.create(requestor= user1,recipient= user2)
    elif len(exists_in_table) != 0:
        #print("It exists in table. Deleting")
        #else delete the friend request since it was a reply to follow back
        exists_in_table.delete()

    data = {'followerID': followerID, 'followeeID': followeeID}
    return HttpResponse(json.dumps(data), content_type="application/json")
    #return HttpResponse()


def unfollow(request):

    if not request.user.is_authenticated:
        return HttpResponseForbidden()

    followerID = request.GET['followerID']
    followeeID = request.GET['followeeID']

    # This should only delete one entry since we have a unique_together
    # constraint on the attributes user1 and user2
    Follow.objects.filter(user1=followerID, user2=followeeID).delete()

     ##check if there is pending friend request from them
    exists_requests = FriendRequest.objects.filter(requestor=followerID,recipient=followeeID)
    if len(exists_requests) != 0:
        #print("There is a pending request. Deleting")
        exists_requests.delete()

    data = {'followerID': followerID, 'followeeID': followeeID}
    return HttpResponse(json.dumps(data), content_type="application/json")
    #return HttpResponse()


# Return a boolean stating if user1 follows user2
def follows(user1, user2):

        following = Follow.objects.filter(user1=user1, user2=user2)
        if following:
            return True
        else:
            return False

def friend_requests(request):
    if not request.user.is_authenticated:
        return HttpResponseForbidden()

    friend_reqs = FriendRequest.objects.filter(recipient=request.user)
    #TODO make sure the users are active too
    user_filter = Q()
    for reqs in friend_reqs:
        user_filter = user_filter | Q(username=reqs.requestor)

    data = User.objects.filter(user_filter)
    serialized_data = serializers.serialize('json',data,fields=('username'))
    #print("DATAAAAA: " + serialized_data)
    return HttpResponse(serialized_data, content_type='application/json')
