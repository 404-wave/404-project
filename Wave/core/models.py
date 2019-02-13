from django.db import models

from users.models import User


class Post(models.Model):

    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField()
    content = models.CharField(max_length = 140)
    privacy = models.IntegerField()
    unlisted = models.BooleanField(default=False)

    class Privacy:
        PUBLIC = 1
        ONLY_ME = 2
        FRIENDS = 3
        FOAF = 4

    def __str__(self):
        return str(self.id)


class Comment(models.Model):

    post_id = models.ForeignKey(Post, on_delete=models.CASCADE)
    date = models.DateTimeField()
    content = models.CharField(max_length = 140)

    def __str__(self):
        return str(self.id)
