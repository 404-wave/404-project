from django.shortcuts import render
from django.http import HttpResponseForbidden, HttpResponseNotFound
from django.core.exceptions import ObjectDoesNotExist
from .forms import ProfileChangeForm as changeForm
from django.http import HttpResponseRedirect
from django.urls import reverse
from users.models import User
from friends.views import follows



# TODO: use the REST API once it is established
def home(request):

    return render(request, 'home.html')


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
    if request.user.id is not pk:
        following = follows(request.user.id, pk)

    return render(request, 'profile.html', {'user': user, 'following': following})

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
            return HttpResponseRedirect('http://127.0.0.1:8000/home/profile/') #TODO need to fix this so not hardcoded
        
        #TODO else statement when form isn't valid

    #if not POST, then must be GET'ing the form itself. so pass context
    else:
        form = changeForm(instance=request.user,initial={'first_name':request.user.first_name,
                                                        'last_name':request.user.last_name,
                                                        'email':request.user.email,
                                                        'github':request.user.github})
        
        context = {'form':form}
        return render(request,'profileEdit.html',context)