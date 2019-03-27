from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required

# Create your views here.
from .models import Post
from .forms import PostForm, ImageForm
from users.models import User, Node, NodeSetting
from datetime import datetime

from comments.forms import CommentForm

from comments.models import Comment
from django.contrib.contenttypes.models import ContentType
import base64
from mimetypes import guess_type

import requests

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
    for post in user_posts:
        if isinstance(post, dict):
            ids.append(post.get('id'))
        elif isinstance(post, Post):
            ids.append(post.id)
    if id not in ids:
        #do something here to make it not 404
        return HttpResponseRedirect('/home')
    instance = None
    try:
        # instance = Post.objects.get(id=id)
        instance = Post.objects.get(id=id)
    except Post.DoesNotExist:
        # TODO: This should work if we have an endpoint to get a specific post
        #       eg: /service/author/posts/id?

        #NO UUID in urls?
        #remove in url.py in posts, home.html
        # ##############################################################################
        # for node in Node.objects.all():
        #     url = node.host + '/service/posts/' + str(id) + "?user=" + str(request.user.id)
        #     response = requests.get(url)
        #     if response.status_code == 200:
        #         instance = response.json()
        #         break
        # #################################################################################
        if instance is None:
            return HttpResponseRedirect('/home')

    initial_data = {
        "content_type": instance.get_content_type,
        "object_id": instance.id
    }

    #https://stackoverflow.com/questions/12615154/how-to-get-the-currently-logged-in-users-user-id-in-django
    #Credit: K Z (https://stackoverflow.com/users/853611/k-z)
    current_user = request.user
    user_id = current_user.id
    post_id = instance.id
    home_host = NodeSetting.objects.all()[0]

    # Creates a form to post comments
    comment_form = CommentForm(request.POST or None, initial=initial_data)
    if comment_form.is_valid():
        comment_type = comment_form.cleaned_data.get("content_type")
        content_type = ContentType.objects.get(model=comment_type)
        obj_id = comment_form.cleaned_data.get("object_id")
        content_data = comment_form.cleaned_data.get("content")
        # parent_obj = None
        # try:
        #     parent_id = int(request.POST.get("parent_id"))
        # except:
        #     parent_id = None
        # if parent_id:
        #     parent_querySet = Comment.objects.filter(id=parent_id)
        #     if parent_querySet.exists() and parent_querySet.count() == 1:
        #         parent_obj = parent_querySet.first()

        # new_comment, created = Comment.objects.get_or_create(
        #     user=request.user,
        #     content_type=content_type,
        #     object_id=obj_id,
        #     content=content_data,
        #     parent=parent_obj

        # )
        for node in Node.objects.all():
            build_endpoint = str(node.host) + "/service/posts/" + str(post_id) + "/comments?user=" + str(current_user.id)
            build_data = {
                "query": "addComment",
                "post": str(node.host) + "/posts/" + str(post_id),
                "comment":{
                    "author":{
                        "id": str(home_host.host) + "/author/" + str(user_id),
                        "host": str(home_host.host) + "/",
                        "url": str(home_host.host) + "/author/" + str(user_id),
                        "github": current_user.github
                    },
                    "comment": content_data,
                    "content_type": content_type,
                    "published": str(datetime.now().isoformat()),
                    "id": str(obj_id)
                }
            }

            #https://www.programcreek.com/python/example/6251/requests.post
            r=requests.post(url=build_endpoint, data=build_data)
            #https://stackoverflow.com/questions/15258728/requests-how-to-tell-if-youre-getting-a-404
            #Credit: Martijn Pieters (https://stackoverflow.com/users/100297/martijn-pieters)
            if r.status_code == 200:
                break
        #change this to go back to post detail?
        #POST OBJECT.get_detail_absolute_url
        #instance.get.....
        print(r)
        return HttpResponseRedirect(instance.get_detail_absolute_url())
        # return HttpResponseRedirect(new_comment.content_object.get_detail_absolute_url())
        # if created:
        #     print("comment worked.")

    #Build and send GET request for comments

    for node in Node.objects.all():
        build_request = node.host + "/service/posts/" + str(post_id) + "/comments?user=" + str(current_user.id)
        r=requests.get(build_request)
        #print(r)
        #https://stackoverflow.com/questions/15258728/requests-how-to-tell-if-youre-getting-a-404
        #Credit: Martijn Pieters (https://stackoverflow.com/users/100297/martijn-pieters)
        if r.status_code == 200:
            break

    # build_request = "https://myblog-cool.herokuapp.com/service/posts/?author_uuid=" + str(current_user.id)
    # r=requests.get(build_request)
    # print(r)
    response = r.json()
    print(response)
    #Parse date into more readbale format
    #https://stackoverflow.com/questions/18795713/parse-and-format-the-date-from-the-github-api-in-python
    #Credit: IQAndreas (https://stackoverflow.com/users/617937/iqandreas)
    for item in response:
        #https://stackoverflow.com/questions/48274898/python3-parsing-datetime-in-format-2018-01-14t235527-337z
        #Credit: Sean Francis N. Ballais (https://stackoverflow.com/users/1116098/sean-francis-n-ballais)
        date = datetime.strptime(item['published'], "%Y-%m-%dT%H:%M:%S.%fZ")
        item['published'] = date.strftime('%A %b %d, %Y at %H:%M GMT')
    #for item in response:
        #print(item['comment'])
    #print(response[0]['author'])
    #build_request = "https://obscure-lake-45818.herokuapp.com/service/posts/d9753910-a6a1-4b78-b53f-71b721027e59/comments?user=20bdb9a6-33d5-4a14-9368-33019d4c2afa"
    #r=requests.get(build_request)
    #print(r)
    #response = r.json()
    #print(response[0])

    #comments = instance.comments

    context = {
        "user": instance.user,
        "instance": instance,
        "comments": response,
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
