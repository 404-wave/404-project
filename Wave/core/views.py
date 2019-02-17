from django.shortcuts import render
from django.http import HttpResponseForbidden, HttpResponseNotFound
from django.core.exceptions import ObjectDoesNotExist


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
