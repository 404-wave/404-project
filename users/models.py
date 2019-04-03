from django.contrib.auth.models import AbstractUser
from django.db import models

import uuid


class User(AbstractUser):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    is_active = models.BooleanField(('active'), default=False)
    is_admin = models.BooleanField(('admin'), default=False)
    is_node = models.BooleanField(('node'), default=False)
    github = models.TextField(max_length=500, blank=True)
    host = models.TextField(max_length=500, blank=False)
    url = models.TextField(max_length=500, blank=True)
    bio = models.TextField(max_length=500, blank=True)

    def __str__(self):
        return self.username

    def to_dict_object_post(self):
        opts = self._meta
        data = {}
        data['id'] = str(self.id)
        data['host'] = self.host
        data['displayName'] = self.username
        data['github'] = self.github
        return data



class Node(models.Model):

    host = models.CharField(max_length = 500)
    sharing = models.BooleanField(default=True)
    username = models.CharField(max_length = 500)
    password = models.CharField(max_length = 500)

    def __str__(self):
        return str(self.host)


class NodeSetting(models.Model):

    id = models.IntegerField(default=1, primary_key=True)
    share_posts = models.BooleanField(default=True, help_text=
        'Specify if posts should be shared with other servers.')
    share_imgs = models.BooleanField(default=True, help_text=
        'Specify if images should be shared with other servers.')
    host = models.CharField(max_length=500)

    # Override database save method to force a max of one entry in the table
    def save(self, *args, **kwargs):
        if NodeSetting.objects.count() == 1:
            NodeSetting.objects.all()[0].delete()
        super(NodeSetting, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.id)
