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
import requests
from requests.auth import HTTPBasicAuth
from users.models import Node

"""
    Shows the details about a post.
    Allows use to post comments under the post.

"""


@login_required(login_url='/login')
def posts_detail(request, id):

    # Checks if the posts is from the user who posted it
    # And if it can be seen by the acessible users
    # If not redirects the user back to the home page
    user_posts = Post.objects.filter_user_visible_posts(
        request.user, remove_unlisted=False)
    ids = []
    current_id_found = False
    for post in user_posts:
        if isinstance(post, dict):
            ids.append(str(post.get('id')))
        elif isinstance(post, Post):
            ids.append(str(post.id))
        if ids[-1] == str(id):
            current_id_found = True
    print("Current Id Found: " + str(current_id_found))
    if str(id) not in ids and not current_id_found:
        print("the given id" + str(id) + "not present in ids" + str(ids))
        return HttpResponseRedirect('/home')
    instance = None
    try:
        # instance = Post.objects.get(id=id)
        instance = Post.objects.get(id=id)
    except Post.DoesNotExist:

        # This should work if we have an endpoint to get a specific post
        #       eg: /service/posts/{POST_ID}/
        # instance is a dictionary and if yes, then comments should be instance[‘comments’]

        for node in Node.objects.all():
<<<<<<< HEAD
=======
            url = node.host + "/service/posts/{0}".format(str(id))

            # test_url = 'https://local:localpassword@cmput-404-proj-test.herokuapp.com/service/posts/{0}'.format(  str(id))
            # print("This is my request id", request.user.id)
            # print(test_url)
            # response = requests.get(test_url, headers=headers)
            # response = requests.get(test_url, headers=headers, auth = HTTPBasicAuth('local', 'localpassword'))

>>>>>>> origin
            headers = {
                'Accept': 'application/json',
                'X-UUID': str(request.user.id)
            }
<<<<<<< HEAD
            url = node.host + "/service/posts/"
            response = requests.get(url, headers=headers, auth=HTTPBasicAuth(
                str(node.username), str(node.password)))
=======
            response = requests.get(url, headers=headers, auth=HTTPBasicAuth(str(node.username), str(node.password)))
>>>>>>> origin
            print(url)
            print("Status code: " + str(response.status_code))

            if response.status_code == 200:
                instance = response.json()
                print("Response from server")
                print(instance)
                print(len(instance['posts']))
                if isinstance(instance.get('posts', None), list) and len(instance['posts']) == 1:
                    instance = instance['posts'][0]
                break

        if instance is None:
            print("Instance is none. Redirecting")
            return HttpResponseRedirect('/home')

    # if instance is a dictionary, then comments should be instance[‘comments’]
    if isinstance(instance, dict):
        content_type = instance['contentType']
    else:
        content_type = instance.get_content_type

    initial_data = {
        "content_type": content_type,
        "object_id": id
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

            user=request.user.id,
            content_type=content_type,
            object_id=obj_id,
            content=content_data,
            parent=parent_obj


        )
        return HttpResponseRedirect(new_comment.content_object.get_detail_absolute_url())
        if created:
            print("comment worked.")

    if isinstance(instance, dict):
        comments = instance['comments']
    else:
        comments = instance.comments

    # TODO: instance.user really should be the username of the person who made
    # the comment. But this could be someone from a different server, so we need
    # to firstly check to see if there is a user on our server with user_id, or
    # scan the node table to see if the user exists somewhere else, then get
    # their username.

    context = {
        "user": request.user,
        "instance": instance,
        "comments": comments,
        "comment_form": comment_form
    }
    return render(request, "posts_detail.html", context)

# https://stackoverflow.com/questions/44489375/django-have-admin-take-image-file-but-store-it-as-a-base64-string
# Credit: Ykh(https://stackoverflow.com/users/6786283/ykh)


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
        # make it unlisted here
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

    # Give an image form if it is an image post
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

        # instance.is_image == True and instance.image is if you want to change one image to another image
        # instance.is_image == False and instance.image is if you are changing from a text post to an image post
        # this way if image field is blank and you click share, it just doesn't change anything
        if (instance.is_image == True and instance.image) or (instance.is_image == False and instance.image):
            # https://stackoverflow.com/questions/44489375/django-have-admin-take-image-file-but-store-it-as-a-base64-string
            # Credit: Ykh(https://stackoverflow.com/users/6786283/ykh)
            image_type, encoded_string = image_to_b64(instance.image)
            instance.content = encoded_string
            instance.data_uri = "data:" + image_type + ";base64," + encoded_string
            instance.is_image = True
            # make it unlisted here
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
