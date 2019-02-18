from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect

# Create your views here.
from .models import Post
from .forms import PostForm
from users.models import User
from datetime import datetime

# def posts_index(request):
#     return HttpResponse("<h1> Hello. You're at the posts index. </h1>")


def posts_create(request):
    # return HttpResponse("<h1> Create a posts. </h1>")
    form = PostForm(request.POST or None)

    if form.is_valid():
        instance = form.save(commit=False)
        instance.user = request.user
        instance.publish = datetime.now()
        instance.save()

    context = {
        "form": form
    }

    # if request.method == "POST":
    #     print("This is the content: ", request.POST.get("content"))
    return render(request, "post_form.html", context)


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
    # TODO: Privacy stuff
    queryset = Post.objects.all()
    context = {
        "object_list": queryset,
        "user": "username"
    }
    return render(request, "posts.html", context)


def posts_update(request, id=None):
    return HttpResponse("<h1> Update a posts. </h1>")
    # instance = get_object_or_404(Post, id=id)
    # form = PostForm(request.POST or None, instance=instance)
    # if form.is_valid():
    #     instance = form.save(commit=False)
    #     instance.user = request.user
    #     instance.publish = datetime.now()
    #     instance.save()
    #    return HttpResponseRedirect(instance.get_absolute_url())
    # context = {
    #     "user": instance.user,
    #     "instance": instance,
    #     "form": form
    # }
    # return render(request, "posts_form.html", context)
    pass


def posts_delete(request, id=None):
    # return HttpResponse("<h1> Delete a posts. </h1>")
    # instance = get_object_or_404(Post, id=id)
    # instance.delete()
    # return HttpResponseRedirect(instance.get_absolute_url())
    # return redirect("")
    pass
