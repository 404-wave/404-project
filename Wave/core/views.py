from django.shortcuts import render

from django.core import serializers
from django.http import HttpResponse, JsonResponse
import json

from users.models import User

def home(request):
    # TODO: If the user is not authenticated then don't show the home page,
    # but instead show soe other page reporting the error. (Maybe just the login page).
    return render(request, 'home.html')


# TODO: use the REST API once it is established
# Just get a list of Users on the server, minus the user making the request
def find(request):

    server_users = serializers.serialize('json', User.objects.exclude(pk=request.user.id))
    return HttpResponse(server_users, content_type="application/json")

# Get a list of Users who the current user follows
def following(request):

    data = dict()
    return JsonResponse(data)


# Get a list of Users who the current user is friends with
def friends(request):

    data = dict()
    return JsonResponse(data)
