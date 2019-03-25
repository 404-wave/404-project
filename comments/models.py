from django.db import models
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
import uuid
import requests

# Create your models here.


class CommentManager(models.Manager):
    def all(self):
        query_set = super(CommentManager,self).filter(parent=None)
        return query_set


    def filter_by_instance(self, instance):
        content_type = ContentType.objects.get_for_model(instance.__class__)
        obj_id = instance.id
        #print("obj_id is: " + str(obj_id))
        query_set = super(CommentManager, self).filter(content_type=content_type, object_id=obj_id).filter(parent=None)
        return query_set

    def get_comments(self, instance):
        #need post id, host name, user id
        #build_request = "https://cmput404-wave.herokuapp.com/service/posts/" + str(32) + "/comments"
        #build_request = "https://desolate-refuge-32192.herokuapp.com/posts/ae29e231-86a0-431b-88f1-ecbc1adfc569/comments"
        #build_request = "https://myblog-cool.herokuapp.com/service/posts"
        #build_request = "https://cmput404-i5.herokuapp.com/posts/fd52adfa-ba32-460b-8e8c-780ce5be6e57/comments"
        #build_request = "https://cmput404w19-project.herokuapp.com/posts"
        #https://cmput404-i5.herokuapp.com/posts/fd52adfa-ba32-460b-8e8c-780ce5be6e57/comments
        #build_request = "https://obscure-lake-45818.herokuapp.com/posts/ca4b9d6a-3b0d-48d0-a4ec-8bdf4e4fd823/comments"
        #build_request = "https://obscure-lake-45818.herokuapp.com/service/posts"
        #build_request = "https://cmput404w19-project.herokuapp.com/posts"
        #Loop through all nodes and make API call, if one is not 404, then use that one
        build_request = "https://obscure-lake-45818.herokuapp.com/service/posts/d9753910-a6a1-4b78-b53f-71b721027e59/comments?user=20bdb9a6-33d5-4a14-9368-33019d4c2afa"
        
        r=requests.get(build_request)
        print(r)
        response = r.json()
        print(response)
        return response


class Comment(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    parent = models.ForeignKey("self", on_delete=models.CASCADE, null=True, blank=True)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.CharField(max_length=36)
    content_object = GenericForeignKey('content_type', 'object_id')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    objects = CommentManager()

    def __str__(self):
        return str(self.user.username)

    class Meta:
        ordering = ['timestamp']

    # replies
    def children(self):
        return Comment.objects.filter(parent=self)


    @property
    def is_parent(self):
        if self.parent is not None:
            return False
        return True
