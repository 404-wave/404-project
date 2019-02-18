from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404

# Create your views here.
from .models import Post
from users.models import User

# def posts_index(request):
#     return HttpResponse("<h1> Hello. You're at the posts index. </h1>")


def posts_create(request):
    return HttpResponse("<h1> Create a posts. </h1>")


def posts_detail(request, id):
    instance = get_object_or_404(Post, id=id)
    context = {
        "user": instance.user,
        "instance": instance
    }
    return render(request, "posts_detail.html", context)
    # return HttpResponse("<h1> Detail a posts. </h1>")


def posts_list(request):
    # return HttpResponse("<h1> List a posts. </h1>")
    queryset = Post.objects.all()
    context = {
        "object_list": queryset,
        "user": "username"
    }
    return render(request, "posts.html", context)


def posts_update(request):
    return HttpResponse("<h1> Update a posts. </h1>")


def posts_delete(request):
    return HttpResponse("<h1> Delete a posts. </h1>")
