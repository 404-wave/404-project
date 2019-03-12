from django.db import models
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
# Create your models here.

# from posts.models import Post


class CommentManager(models.Manager):
    def all(self):
        query_set = super(CommentManager,self).filter(parent=None)
        return query_set


    def filter_by_instance(self, instance):
        content_type = ContentType.objects.get_for_model(instance.__class__)
        obj_id = instance.id
        query_set = super(CommentManager, self).filter(content_type=content_type, object_id=obj_id).filter(parent=None)
        return query_set


class Comment(models.Model):

    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    # post = models.ForeignKey(Post, on_delete=models.CASCADE)
    parent = models.ForeignKey("self", on_delete=models.CASCADE, null=True, blank=True)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)

    # TODO: Maybe should change the content of this to be some type of enum, rather than a textfield.
    contentType = models.TextField(max_length=13, default="text/plain") # Could also be "text/markdown"

    object_id = models.PositiveIntegerField()
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
