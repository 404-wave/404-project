
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect

from posts.models import Post
from posts.forms import PostForm
from users.models import User
from datetime import datetime

from django.shortcuts import render
from django.http import HttpResponseForbidden, HttpResponseNotFound
from django.core.exceptions import ObjectDoesNotExist



from users.models import User
from friends.views import follows



# TODO: use the REST API once it is established
def home(request):

    # TODO: If the user is not authenticated then don't show the home page,
    # but instead show soe other page reporting the error. (Maybe just the login page).

    # Searches for content
    # Needs to search for user name as well
    # Needs a way to show the searched results
    # Should use pagination
    ###################################################################################
    queryset_list = Post.objects.all()
    query = request.GET.get("query")
    if query:
        queryset_list = queryset_list.filter(content__icontains=query)
        print("These are the q's", queryset_list)
    #####################################################################################

    if request.method == "POST":
        form = PostForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = request.user
            instance.publish = datetime.now()
            instance.save()
        queryset = Post.objects.all().order_by("-timestamp")
        user = request.user
        context = {
            "object_list": queryset,
            "user": user,
            "form": form
        }
    else:
        form = PostForm()
        user = request.user
        queryset = Post.objects.all().order_by("-timestamp")
        context = {
            "object_list": queryset,
            "user": user,
            "form": form
        }

    return render(request, "home.html", context)


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

