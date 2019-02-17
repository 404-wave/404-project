from django.db import models
from django.conf import settings
# Create your models here.

from posts.models import Post


class Comment(models.Model):

    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField()

    def __str__(self):
        return str(self.user.username)
