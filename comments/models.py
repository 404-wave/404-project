from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.conf import settings
from django.db import models

import uuid


class CommentManager(models.Manager):

    def all(self):
        query_set = super(CommentManager, self).filter(parent=None)
        return query_set

    def filter_by_instance(self, instance):
        content_type = ContentType.objects.get_for_model(instance.__class__)
        obj_id = instance.id
        query_set = super(CommentManager, self).filter(
            content_type=content_type, object_id=obj_id).filter(parent=None)
        return query_set


class Comment(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    parent = models.ForeignKey(
        "self", on_delete=models.CASCADE, null=True, blank=True)

    user = models.UUIDField(default=uuid.uuid4)

    parent = models.ForeignKey("self", on_delete=models.CASCADE, null=True, blank=True)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    content_object = GenericForeignKey('content_type', 'object_id')
    content = models.TextField()
    published = models.DateTimeField(auto_now_add=True)
    object_id = models.CharField(max_length=36)

    objects = CommentManager()

    def __str__(self):
        return str(self.id)

    class Meta:
        ordering = ['published']

    # replies
    def children(self):
        return Comment.objects.filter(parent=self)

    @property
    def is_parent(self):
        if self.parent is not None:
            return False
        return True
