from django.http import HttpResponse
from django.core import serializers
from django.http import HttpResponseForbidden
from django.conf import settings
from django.shortcuts import render
from django.db.models import Q
import json
import os
import re
import requests
import core.views
import traceback
from users.models import User, Node
from friends.models import Follow, FriendRequest, FriendRequestManager, FollowManager
from requests.auth import HTTPBasicAuth


# Just get a list of Users on the server, minus the user making the request
def find(request):

    if not request.user.is_authenticated:
        return HttpResponseForbidden()

    server_users = User.objects.exclude(pk=request.user.id).filter(is_active=True)

    data = serializers.serialize('json', server_users, fields=('username', 'host'))

    return HttpResponse(data, content_type="application/json")


# Get a list of Users who the current user follows
def following(request):

    if not request.user.is_authenticated:
        return HttpResponseForbidden()

    following = list()
    following_obj = Follow.objects.filter(user1=request.user.id)

    if following_obj:
        for followings in following_obj:
            user = User.objects.filter(id=followings.user2)
            if not user:
                user = get_user(followings.user2_server,followings.user2)
                if user is None:
                    continue  
            else:
                user=user.get()
            following.append(user)

    data = serializers.serialize('json', following, fields=('username',"host"))
    return HttpResponse(data, content_type="application/json")

# Get a list of Users who follow the current user
def followers(request):

    if not request.user.is_authenticated:
        return HttpResponseForbidden()

    # Look at Follow table results where I am the followee
    # followers = User.objects.filter(follower__user2=request.user.id, is_active=True)
    follower_obj = Follow.objects.filter(Q(user2=request.user.id))
    followers = list()
    
    if follower_obj:
        for follower in follower_obj:
            user = User.objects.filter(id=follower.user1)
            if not user:
                user = get_user(follower.user1_server,follower.user1)
                if user is None:
                    continue
            else:
                user=user.get()
            followers.append(user)
    
    data = serializers.serialize('json', followers, fields=('username','host'))
    return HttpResponse(data, content_type="application/json")

# Get a list of Users who the current user is friends with
def friends(request):
    if not request.user.is_authenticated:
        return HttpResponseForbidden()
    follow_manager = FollowManager()
    friendlist = follow_manager.get_friends(request.user)
    dict_friends = {"friends": friendlist}
    return HttpResponse(json.dumps(dict_friends), content_type="application/json") 

def follow(request):
    if not request.user.is_authenticated:
        return HttpResponseForbidden()
    followerID = request.GET['followerID']
    followeeID = request.GET['followeeID']
    followerUser = request.GET['followerUser']
    followeeUser = request.GET['followeeUser']
    followerServer = request.GET['followerserver']
    followeeServer = request.GET['followeeserver']

    user1 = followerID
    user2 = followeeID
    if not (Follow.objects.filter(user1=followerID,user2=followeeID)):
        Follow.objects.create(user1=followerID, user1_server = followerServer,  
        user2=followeeID, user2_server = followeeServer)

     ####add into FriendRequest table####
    #Query to see if the person they want to follow is already following requestor
    exists_in_table = FriendRequest.objects.filter(requestor=user2,recipient=user1)

    if (len(exists_in_table) == 0) & (follows(user2,user1) == False):
        FriendRequest.objects.create(requestor= user1, requestor_server = followerServer,recipient= user2, recipient_server = followeeServer)
    elif len(exists_in_table) != 0:
        exists_in_table.delete()
    
    nodes = Node.objects.all()
    nodeList = dict()
    for node in nodes:
        nodeList[node.host]= {
            'sharing':node.sharing,
            'username':node.username,
            'password':node.password,
        }

    data = {'followerID': followerID,
             'followeeID': followeeID,
             'followerUser': followerUser,
             'followeeUser':followeeUser,
            'followerServer': followerServer,
            'followeeServer': followeeServer,
            'nodes': nodeList
            }
    return HttpResponse(json.dumps(data), content_type="application/json")
    #return HttpResponse()

def getNodeList(request):
    nodes = Node.objects.all()
    nodeList = dict()
    for node in nodes:
        nodeList[node.host]= {
            'sharing':node.sharing,
            'username':node.username,
            'password':node.password,
        }
    return HttpResponse(json.dumps(nodeList),content_type="application/json")

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
        exists_requests.delete()

    data = {'followerID': followerID, 'followeeID': followeeID}
    return HttpResponse(json.dumps(data), content_type="application/json")
    #return HttpResponse()


# Return a boolean stating if user1 follows user2
def follows(user1ID, user2ID):

        following = Follow.objects.filter(user1=user1ID, user2=user2ID)
        if following:
            return True
        else:
            return False


def friend_requests(request):
    if not request.user.is_authenticated:
        return HttpResponseForbidden()
    friendrequest = FriendRequestManager()
    friendList = friendrequest.get_friend_requests(request.user)
    print (friendList)
    dict_friends = {"friends": friendList}
    return HttpResponse(json.dumps(dict_friends), content_type='application/json')

def change_ModelDatabase(request):
    
    localUserID = request.POST.get('local')
    foreignUserID = request.POST.get('foreign')
    follows_too = request.POST.get('follows')

    FriendRequest.objects.filter(recipient=localUserID,requestor=foreignUserID).delete()

    if(follows_too == 'delete'):
        Follow.objects.filter(user1=foreignUserID,user2=localUserID).delete()
       
    return HttpResponse(status=204)

def strip_host(host):
    re_result = re.search("(^https?:\/\/)(.*)", host)
    if (re_result):
        host = re_result.group(2)
    return host


def get_user(server, id):
    user = User()
    server = standardize_url(server)
    server = server[:-1]
    try:
        node = Node.objects.filter(host = server)[0]
        print (node.username, node.password)
    except:
        print("Couldn't find nodel object through filter")
        return None
    server = server+"/"
    build_request = server+'service/author/'+str(id)
    print (build_request)
    print(id)   

    try:
        r=requests.get(build_request, auth=HTTPBasicAuth(node.username, node.password))
        response = r.json()
    except:
        traceback.print_exc
        print("That user does not exist")
        return None
    user.username = response['displayName']
    user.id = response['id']
    user.host = server
    return user

def standardize_url(server):
    server = server.replace(" ","")
    regex = "(^https?:\/\ /)(.*)"
    http_regex = "^http:\/\/(.*)"
    if server.endswith("/") is False:
        server = server+"/"
    if re.search(http_regex,server) is True:
        server= server.split("http://").pop()
        server = "https://"+server
    elif re.search(regex,server) is False:
        server = "https://"+server
    return server