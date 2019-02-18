from django.http import HttpResponse
from django.shortcuts import render
from posts import views
from posts.models import Post

# TODO: Found a hacky way to display all posts on home page


def home(request):
    # TODO: If the user is not authenticated then don't show the home page,
    # but instead show soe other page reporting the error. (Maybe just the login page).
    return render(request, 'home.html')
