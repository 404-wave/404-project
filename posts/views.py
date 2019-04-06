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
from users.models import Node, NodeSetting
import uuid
from requests.auth import HTTPBasicAuth
import json
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
    node_host = None
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
        #       eg: /posts/{POST_ID}/
        # instance is a dictionary and if yes, then comments should be instance[‘comments’]
        success = False
        for node in Node.objects.all():

            url = node.host + "/posts/{0}".format(str(id))

            # test_url = 'https://local:localpassword@cmput-404-proj-test.herokuapp.com/posts/{0}'.format(  str(id))
            # print("This is my request id", request.user.id)
            # print(test_url)
            # response = requests.get(test_url, headers=headers)
            # response = requests.get(test_url, headers=headers, auth = HTTPBasicAuth('local', 'localpassword'))

            headers = {
                'Accept': 'application/json',
                'X-UUID': str(request.user.id)
            }
            response = requests.get(url, headers=headers, auth=HTTPBasicAuth(str(node.username), str(node.password)))
            print(url)
            print("Status code: " + str(response.status_code))

            if response.status_code == 200:
                instance = response.json()
                print("Response from server")
                instance = catch_bad_api(instance)
                node_host = node


        if instance is None:
            print("Instance is none. Redirecting")
            return HttpResponseRedirect('/home')
    print (instance)
    print ()
    print ()
    # if instance is a dictionary, then comments should be instance[‘comments’]
    # if instance is a dictionary, then comments should be instance[‘comments’]
    if isinstance(instance, Post):
        content_type = instance.get_content_type
       
    else:
        if (isinstance(instance, list)):
            instance = instance[0]
        content_type = instance['contentType']

    initial_data = {
        "content_type": content_type,
        "object_id": id
    }

    #https://stackoverflow.com/questions/12615154/how-to-get-the-currently-logged-in-users-user-id-in-django
    #Credit: K Z (https://stackoverflow.com/users/853611/k-z)
    current_user = request.user
    user_id = current_user.id

    if isinstance(instance, dict):
        post_id = instance['id']
    else:
        post_id = instance.id

    home_host = NodeSetting.objects.all()[0]
    # Creates a form to post comments
    comment_form = CommentForm(request.POST or None, initial=initial_data)
    print ("werwer", comment_form.is_valid())
    if comment_form.is_valid():
        comment_type = comment_form.cleaned_data.get("content_type")
        obj_id = comment_form.cleaned_data.get("object_id")
        content_data = comment_form.cleaned_data.get("content")
        parent_obj = None

        # This is an example of a hardcoded POST request
        # build_endpoint = "https://cmput404-wave.herokuapp.com/service/posts/3f46f9c3-256f-441c-899e-928b095df627/comments/"
        # headers = {
        #             'Accept':'application/json',
        #             'X-UUID': '62892c46-7eab-44b9-b106-8524686adfae'
        #         }
        # build_data = {
        #     "query": "addComment",
        #     "post": "https://cmput404-wave.herokuapp.com/service/posts/3f46f9c3-256f-441c-899e-928b095df627",
        #     "comment": {
        #         "author":{
        #             "id": "http://127.0.0.1:8000/service/author/62892c46-7eab-44b9-b106-8524686adfae",
        #             "host": "http://127.0.0.1:8000",
        #             "url": "http://127.0.0.1:8000/service/author/62892c46-7eab-44b9-b106-8524686adfae",
        #             "github": ''
        #         },
        #         "comment": "test post for deployment",
        #         "content_type": "text/plain",
        #         "published": str(datetime.now().isoformat()),
        #         "id": str(uuid.uuid4())
        #     }
        # }
        # r=requests.post(url=build_endpoint, json=build_data, headers=headers, auth=HTTPBasicAuth(str('local'), str('localpassword')))
        success = False
        if (node_host):

   
            #build_endpoint = str(node.host) + "/service/posts/" + "3f46f9c3-256f-441c-899e-928b095df627" + "/comments/"
            #print(build_endpoint)
            build_endpoint = str(node_host.host) + "/service/posts/" + str(post_id) + "/comments/"
            headers = {
                    'Accept':'application/json',
                    'X-UUID': str(user_id)
                }
            #print("build_endpoint is: " + str(build_endpoint))
            build_data = {
                "query": "addComment",
                "post": str(node_host.host) + "/service/posts/" + str(post_id),
                "comment": {
                    "author":{
                        #"id": str(home_host.host) + "/service/author/" + str(user_id),
                        "id": str(user_id),
                        "host": str(home_host.host),
                        "url": str(home_host.host) + "/service/author/" + str(user_id),
                        "github": current_user.github
                    },
                    "comment": content_data,
                    "contentType": "text/plain",
                    "published": str(datetime.now().isoformat()),
                    "id": str(uuid.uuid4())
                }
            }
            #print("build_data is: " + str(build_data))
            #https://www.programcreek.com/python/example/6251/requests.post
            r=requests.post(url=build_endpoint, json=build_data, headers=headers, auth=HTTPBasicAuth(str(node_host.username), str(node_host.password)))
            print("POSTing comment to host: " + str(node_host.host))
            print (build_endpoint)
            print("Status code for comment POST: " + str(r.status_code))


            #print(r)
            #https://stackoverflow.com/questions/15258728/requests-how-to-tell-if-youre-getting-a-404
            #Credit: Martijn Pieters (https://stackoverflow.com/users/100297/martijn-pieters)
            #Partner group can return "Post Not Found"
            success = json.loads(r.content)['success']

        if success:
            redirect_url = str(home_host.host) + '/posts/detail/' + str(post_id)
            return redirect(redirect_url)
        else:
            print ("WEWPPP", obj_id)
            #content_type = ContentType.objects.get(model=comment_type)
            #for_concrete_model=False
            content_type = ContentType.objects.get_for_model(Post())
            new_comment, created = Comment.objects.get_or_create(

                user=request.user.id,
                content_type=content_type,
                object_id=obj_id,
                content=content_data,
                parent=parent_obj


            )
            redirect_url = str(home_host.host) + '/posts/detail/' + str(post_id)
            return redirect(redirect_url)
        # if created:
        #     print("comment worked.")

    if isinstance(instance, dict):
        comments = instance['comments']
        print(comments)
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


def catch_bad_api(instance):
    try:
        instance['posts']
        if isinstance(instance.get('posts', None), list) and len(instance['posts']) == 1:
            instance = instance['posts'][0]
        return instance

    except:
        return instance

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
        instance.content = "data:" + image_type + ";base64," + encoded_string
        instance.content_type = image_type + ";base64"
        #instance.data_uri = "data:" + image_type + ";base64," + encoded_string
        instance.is_image = True
        # make it unlisted here
        #instance.unlisted = True
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
            #instance.unlisted = True
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
