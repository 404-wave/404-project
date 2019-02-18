from django.db import models

from users.models import User


class Post(models.Model):

    PUBLIC = 0
    PRIVATE = 1
    FRIENDS = 2
    FOAF = 3
    ONLY_SERVER = 4
    ONLY_ME = 5

    Privacy = (
        (PUBLIC, 'Public'),
        (PRIVATE, 'Only certain friends'),
        (FRIENDS, 'Only friends'),
        (FOAF, 'Friend of a friend'),
        (ONLY_SERVER, 'Server wide'),
        (ONLY_ME, 'Only me')
    )

    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField()
    content = models.CharField(max_length = 140)
    privacy = models.IntegerField(choices=Privacy, default=PUBLIC)
    unlisted = models.BooleanField(default=False)

    def __str__(self):
        return str(self.id)


class Comment(models.Model):

    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    post_id = models.ForeignKey(Post, on_delete=models.CASCADE)
    date = models.DateTimeField()
    content = models.CharField(max_length = 140)

    def __str__(self):
        return str(self.id)
