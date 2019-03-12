from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required

# Create your views here.
from .models import Post
from .forms import PostForm
from users.models import User
from datetime import datetime

from comments.forms import CommentForm

from comments.models import Comment
from django.contrib.contenttypes.models import ContentType

@login_required(login_url='/login')
def posts_detail(request, id):
    instance = get_object_or_404(Post, id=id)

    user_posts = Post.objects.filter_user_visible_posts(request.user, remove_unlisted=False)
    try: 
        user_posts.get(id=instance.id)
    except Post.DoesNotExist:
        return HttpResponseRedirect('/home')

    initial_data = {
        "content_type": instance.get_content_type,
        "object_id": instance.id
    }
    comment_form = CommentForm(request.POST or None, initial=initial_data)
    if comment_form.is_valid():
        comment_type = comment_form.cleaned_data.get("content_type")
        content_type = ContentType.objects.get(model=comment_type)
        obj_id = comment_form.cleaned_data.get("object_id")
        content_data = comment_form.cleaned_data.get("content")
        parent_obj = None
        try:
            parent_id = int(request.POST.get("parent_id"))
        except:
            parent_id = None
        if parent_id:
            parent_querySet = Comment.objects.filter(id=parent_id)
            if parent_querySet.exists() and parent_querySet.count() == 1:
                parent_obj = parent_querySet.first()

        new_comment, created = Comment.objects.get_or_create(
            user = request.user,
            content_type = content_type,
            object_id = obj_id,
            content = content_data,
            parent = parent_obj

        )
        return HttpResponseRedirect(new_comment.content_object.get_detail_absolute_url())
        if created:
            print("comment worked.")

    comments = instance.comments
    context = {
        "user": instance.user,
        "instance": instance,
        "comments": comments,
        "comment_form": comment_form
    }
    return render(request, "posts_detail.html", context)

@login_required(login_url='/login')
def posts_update(request, id=None):
    # return HttpResponse("<h1> Update a posts. </h1>")
    instance = get_object_or_404(Post, id=id)
    if instance.user != request.user:
        return HttpResponseRedirect(instance.get_detail_absolute_url())
    form = PostForm(request.POST or None,
                    request.FILES or None, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.user = request.user
        instance.publish = datetime.now()
        instance.save()
        return HttpResponseRedirect(instance.get_detail_absolute_url())
    context = {
        "user": instance.user,
        "instance": instance,
        "form": form
    }
    return render(request, "posts_form.html", context)

@login_required(login_url='/login')
def posts_delete(request, id=None):
    # return HttpResponse("<h1> Delete a posts. </h1>")\
    instance = get_object_or_404(Post, id=id)
    if instance.user != request.user:
        return HttpResponseRedirect(instance.get_detail_absolute_url())
    instance.comments.delete()
    instance.delete()
    return redirect("/home/")