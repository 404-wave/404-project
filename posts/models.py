import os
import uuid

from django.db import models
from django.conf import settings
from django.urls import reverse
from comments.models import Comment
from django.contrib.contenttypes.models import ContentType
from users.models import User
from users.models import Node
from django.dispatch import receiver
from django.db.models.signals import post_save, m2m_changed
import base64
from mimetypes import guess_type
import uuid
import json
import requests
from requests.auth import HTTPBasicAuth


# Create your models here.

#https://stackoverflow.com/questions/44489375/django-have-admin-take-image-file-but-store-it-as-a-base64-string
#Credit: Ykh(https://stackoverflow.com/users/6786283/ykh)
def image_to_b64(image_file):
    with open(image_file.path, "rb") as f:
        encoded_string = base64.b64encode(f.read()).decode()
        image_type = guess_type(image_file.path)[0]
        return image_type, encoded_string

def upload_location(instance, filename):
    return "%s/%s" % (instance.id, filename)


class PostManager(models.Manager):

    """
        Functions that were made to test individual privacy setting
    """
    def all(self, *args, **kwargs):
        query_set = super(PostManager, self).order_by("-timestamp")
        return query_set

    def filter_by_public(self, *args, **kwargs):
        query_set = super(PostManager, self).filter(privacy=0).order_by("-timestamp")
        return query_set

    def filter_by_friends(self, *args, **kwargs):
        followers = User.objects.filter(follower__user2=user.id, is_active=True)
        following = User.objects.filter(followee__user1=user.id, is_active=True)
        friends = following & followers
        query_set = super(PostManager, self).filter(privacy=2, user__in=friends).order_by("-timestamp")
        return query_set

    def filter_by_foaf(self, *args, **kwargs):
        friends_followers = User.objects.filter(follower__user2__in=friends, is_active=True)
        friends_following = User.objects.filter(followee__user1__in=friends, is_active=True)
        friends_of_friends = friends_followers &  friends_following
        query_set = super(PostManager, self).filter(privacy=3, user__in=friends_of_friends).order_by("-timestamp")
        return query_set

    def filter_by_only_me(self, *args, **kwargs):
        user = kwargs.pop('user')
        print("This is a user", user)
        query_set = super(PostManager, self).filter(privacy=5, user=user).order_by("-timestamp")
        return query_set


    """
        Filters all posts based on the privacy setting chosen.
        Posts are uniquely filtered for a users
    """
    def filter_user_visible_posts(self, user, *args, **kwargs):



        # TODO: This is for getting post from another node
        ####################################################################

        """
            When you make requests to our partner group for posts and comments
            you need to include an additional query parameter for the _requesting user’s_ UUID.
            Ex: /author/posts/

        """

        posts_from_servers = []
        for node in Node.objects.all():
            url = node.host + "/author/posts/"
            # test_url = 'https://cmput-404-proj-test.herokuapp.com/author/posts/'

            try:
                headers = {
                    'Accept':'application/json',
                    'X-UUID': str(user.id)
                }
                print("This is my: ", user.id)
                # response = requests.get(test_url, headers=headers, auth=HTTPBasicAuth('local', 'localpassword'))
                response = requests.get(url, headers=headers, auth=HTTPBasicAuth(str(node.username), str(node.password)))

                print()
                print(response)
                print()
                # print(test_url)
                print(url)
                print(response.status_code)
                if (response.status_code > 199 and response.status_code <300):
                    responselist = response.json()
                    print("CONTENT:")
                    print(response.content)
                    print()
                    print()
                    print(responselist["posts"][1]["content"])
                    print(responselist["posts"][0]["content"])
                    print()
                    print()
                    #if servers are bad and don't include the author server we do
                    for item in responselist["posts"]:
                        if (item['author']['host'] == ''):
                            print ("ADDING HOST")
                            item['author']['host'] = node.host
                    # if responselist["posts"][0]["author"]["host"] == '':
                    #     responselist["posts"][0]["author"]["host"] = node.host
                    posts_from_servers.extend(responselist["posts"])
            except Exception as e:
                print(e)
                print(e)
                print(e)
                pass


            #print(response.json())
            #posts_from_servers.extend(response.json())
        ####################################################################

        only_me_posts = super(PostManager, self).filter(privacy=5, user=user)
        public_posts = super(PostManager, self).filter(privacy=0)

        private_posts = user.accessible_posts.all()

        followers = User.objects.filter(follower__user2=user.id, is_active=True)
        following = User.objects.filter(followee__user1=user.id, is_active=True)
        friends = following & followers
        friends_posts = super(PostManager, self).filter(privacy=2, user__in=friends)



        friends_followers = User.objects.filter(follower__user2__in=friends, is_active=True)
        friends_following = User.objects.filter(followee__user1__in=friends, is_active=True)
        friends_of_friends = friends_followers &  friends_following
        friends_of_friends_posts = super(PostManager, self).filter(privacy=3, user__in=friends_of_friends)

        server_only_posts =  super(PostManager, self).filter(privacy=4, user = user)


        all_posts = only_me_posts | public_posts | friends_posts | friends_of_friends_posts | private_posts | server_only_posts

        """
            If unlisted is passed as True, the function will remove unlisted posts from the list.
            If it is passed as False, then it will not remove the unlisted posts.
        """
        if kwargs.get('remove_unlisted', True):
            all_posts = all_posts.filter(unlisted=False)
        all_posts = list(all_posts.order_by('-timestamp'))
        all_posts.extend(posts_from_servers)

        return all_posts

    def filter_user_visible_posts_by_user_id(self, user_id, server_only, *args, **kwargs):

        # NOTE: Don't add this here right now.

        # This is for getting post from another node
        ####################################################################
        # posts_from_servers = []
        # for node in Node.objects.all():
        #     response = requests.get(node.host + "?user=" + str(user_id))
        #     posts_from_servers.extend(response.json())
        ####################################################################

        only_me_posts = super(PostManager, self).filter(privacy=5, user=user_id)
        public_posts = super(PostManager, self).filter(privacy=0)

        #private_posts = user.accessible_posts.all()
        # Probably there is a better way to do this. I can't use the line above
        # since it requires a user instance and if the requestor is on another
        # server then they won't have an instance here.
        private_posts = Post.objects.none()
        for post in Post.objects.filter(privacy=1):
            for user in post.accessible_users.all():
                if user.id == user_id:
                    private_posts |= Post.objects.filter(id=post.id)

        followers = User.objects.filter(follower__user2=user_id, is_active=True)
        following = User.objects.filter(followee__user1=user_id, is_active=True)

        friends = following & followers
        friends_posts = super(PostManager, self).filter(privacy=2, user__in=friends)

        friends_followers = User.objects.filter(follower__user2__in=friends, is_active=True)
        friends_following = User.objects.filter(followee__user1__in=friends, is_active=True)
        friends_of_friends = friends_followers & friends_following
        friends_of_friends_posts = super(PostManager, self).filter(privacy=3, user__in=friends_of_friends)

        # Need to pass a boolean because the API might call this function and
        # the request could've came from a different server
        server_only_posts = Post.objects.none()
        if server_only is True:
            server_only_posts =  super(PostManager, self).filter(privacy=4, user=user_id)


        all_posts = only_me_posts | public_posts | friends_posts | friends_of_friends_posts | private_posts | server_only_posts
        # all_posts = list(all_posts).extend(posts_from_servers)

        """
            If unlisted is passed as True, the function will remove unlisted posts from the list.
            If it is passed as False, then it will not remove the unlisted posts.
        """
        return all_posts.order_by('-timestamp')


    # TODO: Not sure if this works yet.

    def filter_server_posts(self, user, *args, **kwargs):
        all_posts = self.filter_user_visible_posts(user, server_only=False)
        return all_posts



class Post(models.Model):

    PUBLIC = 0
    PRIVATE = 1
    FRIENDS = 2
    FOAF = 3
    ONLY_SERVER = 4
    ONLY_ME = 5

    Privacy = (
        (PUBLIC, 'PUBLIC'),
        (PRIVATE, 'PRIVATE'),
        (FRIENDS, 'FRIENDS'),
        (FOAF, 'FOAF'),
        (ONLY_SERVER, 'SERVERONLY'),
        (ONLY_ME, 'ONLY ME')
    )

    POST = "Post"
    Status = {
        (POST, 'Post')
    }

    APPLICATION = "application/base64"
    MARKDOWN = "text/markdown"
    JPEG = "image/jpeg;base64"
    PNG = "image/png;base64"
    TEXT = "text/plain"

    ContentType = (
        (TEXT, "text/plain"),
        (MARKDOWN, "text/markdown"),
        (APPLICATION, "application/base64"),
        (JPEG, "image/jpeg;base64"),
        (PNG, "image/png;base64"),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    status = models.CharField(max_length=6, choices=Status, default=POST)
    content = models.TextField(blank=True)
    image = models.FileField(upload_to=upload_location, null=True, blank=True)
    is_image = models.BooleanField(default=False)
    data_uri = models.TextField(blank=True)
    publish = models.DateTimeField(auto_now=False, auto_now_add=False)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)
    privacy = models.IntegerField(choices=Privacy, default=PUBLIC)
    unlisted = models.BooleanField(default=False)
    accessible_users =  models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="accessible_posts", blank=True)
    objects = PostManager()

    # Used to determine the content type of the post. Necessary for the API
    # users to understand how to handle the actual content of the post.
    content_type = models.CharField(max_length=18 ,choices=ContentType, default="text/plain")
    title = models.TextField(default = "default_title")
    def __str__(self):
        return str(self.user.username)

    """
        Redirects to the specific urls.
    """
    def get_detail_absolute_url(self):
        return reverse("posts-detail", kwargs={"id": self.id})

    def get_delete_absolute_url(self):
        return reverse("posts-delete", kwargs={"id": self.id})

    def get_absolute_url(self):
        return reverse("home")

    def get_edit_absolute_url(self):
        return reverse("posts-update", kwargs={"id": self.id})

    # Images
    def decodeImage(self, image):
        pass

    def encodeImage(self, image):
        pass

    @property
    def comments(self):
        instance = self
        query_set = Comment.objects.filter_by_instance(instance)
        return query_set

    @property
    def get_content_type(self):
        instance = self
        content_type = ContentType.objects.get_for_model(instance.__class__)
        return content_type

#https://stackoverflow.com/questions/16041232/django-delete-filefield
#Credit: Tony (https://stackoverflow.com/users/247441/tony)

# These two auto-delete files from filesystem when they are unneeded:
# @receiver(models.signals.post_delete, sender=Post)
# def auto_delete_file_on_delete(sender, instance, **kwargs):
#     """
#     Deletes file from filesystem
#     when corresponding `Post` object is deleted.
#     """
#     if instance.image:
#         if os.path.isfile(instance.image.path):
#             os.remove(instance.image.path)

# @receiver(models.signals.pre_save, sender=Post)
# def auto_delete_file_on_change(sender, instance, **kwargs):
#     """
#     Deletes old file from filesystem
#     when corresponding `Post` object is updated
#     with new file.
#     """
#     if not instance.pk:
#         return False

#https://stackoverflow.com/questions/44489375/django-have-admin-take-image-file-but-store-it-as-a-base64-string
#Credit: Ykh(https://stackoverflow.com/users/6786283/ykh)
@receiver(post_save, sender=Post)
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
