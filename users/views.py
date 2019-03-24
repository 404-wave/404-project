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
            user = form.save();
            host = request.scheme + "://" + request.META['HTTP_HOST'] + "/"
            user.url = host + "service/author/" + str(user.id)
            user.host = host
            user.save()
            return HttpResponseRedirect(reverse('login'))
        else :
            form = UserCreationForm(request.POST)
            context = {'form' : form}
            return render(request, 'registration/register.html', context)

    else:
        form = UserCreationForm()
        context = {'form' : form}
        return render(request, 'registration/register.html', context)
