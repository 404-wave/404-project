from django.shortcuts import render
from django.shortcuts import HttpResponseRedirect
from django.template import RequestContext
from django.urls import reverse

from .forms import UserCreationForm
import requests


def index(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('home'))
    else:
        return HttpResponseRedirect(reverse('login'))

def register(request):

    if request.method == 'POST':

        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save();
            return HttpResponseRedirect(reverse('login'))
        else :
            form = UserCreationForm(request.POST)
            context = {'form' : form}
            return render(request, 'registration/register.html', context)

    else:
        form = UserCreationForm()
        context = {'form' : form}
        return render(request, 'registration/register.html', context)

def list_events(request):
    if not request.user.is_authenticated:
        return HttpResponseForbidden()

    else:
        #Should we worry about input sanitation here?
        #print(request.user.github)
        build_request = 'https://api.github.com/users/' + request.user.github + '/events'
        r=requests.get(build_request)
        response = r.json()
        #print(response)
        event_types =[]
        for item in response:
            if item['type'] not in event_types:
                event_types.append(item['type'])
            #repos.append(item['name'])
        #print(repos)
        #print(response)
        #print(response)

        return render(request, 'home.html', {'event_types': event_types})

def event_details(request, event_type):
    if not request.user.is_authenticated:
        return HttpResponseForbidden()

    else:
        build_request = 'https://api.github.com/users/' + request.user.github + '/events'
        r=requests.get(build_request)
        response = r.json()
        #print(response)
        events =[]
        for item in response:
            if item['type'] == event_type:
                events.append(item['repo']['url'])

        return render(request, 'home.html', {'events': events})


def post_repos(request):
    if not request.user.is_authenticated:
        return HttpResponseForbidden()

    else:
        #Should we worry about input sanitation here?
        #print(request.user.github)
        build_request = 'https://api.github.com/users/' + request.user.github + '/repos'
        r=requests.get(build_request)
        response = r.json()
        #print(response)
        repos =[]
        for item in response:
            repos.append(item['name'])
        #print(repos)
        #print(response)
        #print(response)

        return render(request, 'home.html', {'repos': repos, 'github': request.user.github})
