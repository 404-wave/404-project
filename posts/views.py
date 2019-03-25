from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required

# Create your views here.
from .models import Post
from .forms import PostForm, ImageForm
from users.models import User
from datetime import datetime

from comments.forms import CommentForm

from comments.models import Comment
from django.contrib.contenttypes.models import ContentType
import base64
from mimetypes import guess_type

"""
    Shows the details about a post.
    Allows use to post comments under the post.

"""
@login_required(login_url='/login')
def posts_detail(request, id):
    instance = get_object_or_404(Post, id=id)

    # Checks if the posts is from the user who posted it
    # And if it can be seen by the acessible users
    # If not redirects the user back to the home page
    user_posts = Post.objects.filter_user_visible_posts(request.user, remove_unlisted=False)
    try:
        user_posts.get(id=instance.id)
    except Post.DoesNotExist:
        return HttpResponseRedirect('/home')

    initial_data = {
        "content_type": instance.get_content_type,
        "object_id": instance.id
    }

    # Creates a form to post comments
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

#https://stackoverflow.com/questions/44489375/django-have-admin-take-image-file-but-store-it-as-a-base64-string
#Credit: Ykh(https://stackoverflow.com/users/6786283/ykh)
def image_to_b64(image_file):
    with open(image_file.path, "rb") as f:
        encoded_string = base64.b64encode(f.read()).decode()
        image_type = guess_type(image_file.path)[0]
        return image_type, encoded_string

def create_base64_str(sender, instance=None, created=False, **kwargs):
    if instance.image and created:
        image_type, encoded_string = image_to_b64(instance.image)
        instance.content = encoded_string
        instance.data_uri = "data:" + image_type + ";base64," + encoded_string
        instance.is_image = True
        #make it unlisted here
        instance.unlisted = True
        instance.image.delete()
        instance.save()


"""
    Allows the user to update a post.
"""
@login_required(login_url='/login')
def posts_update(request, id=None):


    # Checks if the user who created the post can update the post
    # If not redirect the user
    instance = get_object_or_404(Post, id=id)
    if instance.user != request.user:
        return HttpResponseRedirect(instance.get_detail_absolute_url())

    #Give an image form if it is an image post
    if instance.is_image == False:
        form = PostForm(request.POST or None,
                        request.FILES or None, instance=instance)

    else:
        form = ImageForm(request.POST or None,
                        request.FILES or None, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.user = request.user
        instance.publish = datetime.now()

        #instance.is_image == True and instance.image is if you want to change one image to another image
        #instance.is_image == False and instance.image is if you are changing from a text post to an image post
        #this way if image field is blank and you click share, it just doesn't change anything
        if (instance.is_image == True and instance.image) or (instance.is_image == False and instance.image):
            #https://stackoverflow.com/questions/44489375/django-have-admin-take-image-file-but-store-it-as-a-base64-string
            #Credit: Ykh(https://stackoverflow.com/users/6786283/ykh)
            image_type, encoded_string = image_to_b64(instance.image)
            instance.content = encoded_string
            instance.data_uri = "data:" + image_type + ";base64," + encoded_string
            instance.is_image = True
            #make it unlisted here
            instance.unlisted = True
            instance.image.delete()
        instance.save()
        return HttpResponseRedirect(instance.get_detail_absolute_url())
    context = {
        "user": instance.user,
        "instance": instance,
        "form": form
    }
    return render(request, "posts_form.html", context)


"""
    Allows the user to delete a post
"""

@login_required(login_url='/login')
def posts_delete(request, id=None):

    # Checks if the user who created the post can delete the post
    # If not redirect the user
    instance = get_object_or_404(Post, id=id)
    if instance.user != request.user:
        return HttpResponseRedirect(instance.get_detail_absolute_url())
    instance.comments.delete()
    instance.delete()
    return redirect("/home/")
