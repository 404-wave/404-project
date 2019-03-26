
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect

from posts.models import Post
from posts.forms import PostForm
from users.models import User
from friends.models import FriendRequest
from datetime import datetime
from django.contrib.auth.decorators import login_required

from django.shortcuts import render
from django.http import HttpResponseForbidden, HttpResponseNotFound
from django.core.exceptions import ObjectDoesNotExist

from .forms import ProfileChangeForm as changeForm

from django.urls import reverse

from friends.views import follows

import requests
import re
import pytz

import base64



# TODO: use the REST API once it is established
@login_required(login_url='/login')
def home(request):
	utc=pytz.UTC

	# TODO: If the user is not authenticated then don't show the home page,
	# but instead show soe other page reporting the error. (Maybe just the login page).

	streamlist = []
	instance = None
	if request.method == "POST":
		data = request.POST.copy()
		data['user'] = request.user.id
		data['publish'] = datetime.now()
		form = PostForm(data, request.FILES or None)
		if form.is_valid():
			instance = form.save()
			form = PostForm()
		print(form.errors)
		user = request.user


		privacy = request.GET.get('privacy', None)
		if privacy is not None:
			streamlist = Post.objects.filter(privacy=privacy)
			print("GET", streamlist)
		else:
			streamlist = Post.objects.filter_user_visible_posts(user=request.user)

		"""
			Allows you to search for the titles of post
		"""
		query = request.GET.get("query")
		if query:
			streamlist = streamlist.filter(content__icontains=query)

		print("Stream list len: ", len(streamlist))
		print("Stream list: ", streamlist)

		#Cast QuerySet into a list for Github
		streamlist = list(streamlist)

		#TODO: increase rate limit with OAuth?
		#if so, do pagination of API call
		#make call to Github API
		build_request = 'https://api.github.com/users/' + request.user.github + '/events'
		r=requests.get(build_request)
		response = r.json()

		if r.status_code == 200:
			for event in response:
				#parse through output of API call and formulate into readable message
				event_type = ''
				#Parse event type into multiple words
				#eg: PushEvent -> Push event
				#https://stackoverflow.com/questions/2277352/split-a-string-at-uppercase-letters
				#Credit: Mark Byers (https://stackoverflow.com/users/61974/mark-byers)
				for word in re.findall('[A-Z][^A-Z]*', event['type']):
					event_type += word + ' '
				#Parse date into more readbale format
				#https://stackoverflow.com/questions/18795713/parse-and-format-the-date-from-the-github-api-in-python
				#Credit: IQAndreas (https://stackoverflow.com/users/617937/iqandreas)
				date = datetime.strptime(event['created_at'], "%Y-%m-%dT%H:%M:%SZ")
				event_datetime = date.strftime('%A %b %d, %Y at %H:%M GMT')
				#Parse url
				event_repo = 'https://github.com/' + event['repo']['name']
				message = "You had a " + event_type + 'on ' + event_datetime + ' for repo ' + event_repo

				#Flag for determining if a github event is older than all posts
				is_oldest = True
				#sort based on datetime
				for item in streamlist:
					if isinstance(item, Post):
						#Note that the time returned by the github api is timezone naive
						#We must give it local timezone information in order to compare with timestamp
						#of a post
						#https://stackoverflow.com/questions/15307623/cant-compare-naive-and-aware-datetime-now-challenge-datetime-end
						#Credit: Viren Rajput (https://stackoverflow.com/users/997562/viren-rajput)
						if item.timestamp < utc.localize(date):
							is_oldest = False
							streamlist.insert(streamlist.index(item), message)
							break

				if is_oldest:
					streamlist.append(message)


		context = {
			"object_list": streamlist,
			"user": user,
			"form": form,
		}
	else:

		form = PostForm()
		user = request.user


		privacy = request.GET.get('privacy', None)
		if privacy is not None:
			streamlist = Post.objects.filter(privacy=privacy)
			print("GET", streamlist)
		else:
			streamlist = Post.objects.filter_user_visible_posts(user=request.user)

		"""
			Allows you to search for the titles of post
		"""
		query = request.GET.get("query")
		if query:
			streamlist = streamlist.filter(content__icontains=query)

		#print("Stream list len: ", len(streamlist))
		#print("Stream list: ", streamlist)

		#Cast QuerySet to list for Github
		streamlist = list(streamlist)



		#TODO: increase rate limit with OAuth?
		#if so, do pagination of API call
		#Validate user github?
		#make call to Github API
		build_request = 'https://api.github.com/users/' + request.user.github + '/events'
		r=requests.get(build_request)
		response = r.json()

		if r.status_code == 200:
			for event in response:
				#parse through output of API call and formulate into readable message
				event_type = ''
				#Parse event type into multiple words
				#eg: PushEvent -> Push event
				#https://stackoverflow.com/questions/2277352/split-a-string-at-uppercase-letters
				#Credit: Mark Byers (https://stackoverflow.com/users/61974/mark-byers)
				for word in re.findall('[A-Z][^A-Z]*', event['type']):
					event_type += word + ' '
				#Parse date into more readbale format
				#https://stackoverflow.com/questions/18795713/parse-and-format-the-date-from-the-github-api-in-python
				#Credit: IQAndreas (https://stackoverflow.com/users/617937/iqandreas)
				date = datetime.strptime(event['created_at'], "%Y-%m-%dT%H:%M:%SZ")
				event_datetime = date.strftime('%A %b %d, %Y at %H:%M GMT')
				#Parse url
				event_repo = 'https://github.com/' + event['repo']['name']
				message = "You had a " + event_type + 'on ' + event_datetime + ' for repo ' + event_repo

				#Flag for determining if a github event is older than all posts
				is_oldest = True
				#sort based on datetime
				for item in streamlist:
					if isinstance(item, Post):
						#Note that the time returned by the github api is timezone naive
						#We must give it local timezone information in order to compare with timestamp
						#of a post
						#https://stackoverflow.com/questions/15307623/cant-compare-naive-and-aware-datetime-now-challenge-datetime-end
						#Credit: Viren Rajput (https://stackoverflow.com/users/997562/viren-rajput)
						if item.timestamp < utc.localize(date):
							is_oldest = False
							streamlist.insert(streamlist.index(item), message)
							break

				if is_oldest:
					streamlist.append(message)

		context = {
			"object_list": streamlist,
			"user": user,
			"form": form,
		}
	if instance and instance.unlisted is True:
		context["unlisted_instance"] = instance

	return render(request, "home.html", context)

@login_required(login_url='/login')
def profile(request, pk = None):

	if not request.user.is_authenticated:
		return HttpResponseForbidden()

	# If no pk is provided, just default to the current user's page
	if pk is None:
		pk = request.user.id

	try:
		user = User.objects.get(pk=pk)
	except ObjectDoesNotExist:
		# TODO: Return a custom 404 page
		return HttpResponseNotFound("That user does not exist")

	# Check if we follow the user whose profile we are looking at
	following = False
	button_text = "Unfollow"
	if request.user.id is not pk:
		following = follows(request.user.id, pk)
		if (following == False):
			button_text = "Follow"


	return render(request, 'profile.html', {'user': user, 'following': following, 'button_text': button_text})



@login_required(login_url='/login')
def edit_profile(request):

	if not request.user.is_authenticated:
		return HttpResponseForbidden()

	#if they submitted new changes create change form
	if request.method == "POST":
		form = changeForm(request.POST,instance=request.user)

		#check for validity of entered data. save to db if valid and redirect
		# back to profile page
		if form.is_valid():
			form.save()

			return HttpResponseRedirect(reverse('my_profile')) 	
    
		#TODO else statement when form isn't valid

	#if not POST, then must be GET'ing the form itself. so pass context
	else:
		form = changeForm(instance=request.user,initial={'first_name':request.user.first_name,
														'last_name':request.user.last_name,
														'email':request.user.email,
														'github':request.user.github})

		context = {'form':form}
		return render(request,'profileEdit.html',context)


def friends(request):
	if not request.user.is_authenticated:
		return HttpResponseForbidden()
	user = request.user

	##Friend Requests##
		#Query to see if any pending friend requests
	friend_requests = FriendRequest.objects.filter(recipient=user.id)
	context = {
		'user':user,
		'friend_requests': friend_requests,
	}

	return render(request, 'friends.html', context)
