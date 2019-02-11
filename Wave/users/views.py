from django.shortcuts import render
from django.shortcuts import HttpResponseRedirect
from django.urls import reverse
#from django.contrib.auth.forms import UserCreationForm
from .forms import UserCreationForm

def index(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse("home"))
    else:
        return HttpResponseRedirect(reverse("login"))
# Create your views here.
def register(request):

    # TODO: We will need a custom user creation form to hanlde all of the
    # required inputs
    form = UserCreationForm()
    context = {'form' : form}
    return render(request, 'registration/register.html', context)
