from django.db import models

from users.models import User


class Follow(models.Model):
    #user1 is follower , user2 is followee
    user1 = models.UUIDField()
    user2 = models.UUIDField()

    class Meta:
        unique_together = (('user1', 'user2'), )

    def __str__(self):
        return str(self.id)

class FriendRequest(models.Model):

    requestor = models.UUIDField()
    recipient = models.UUIDField()

    class Meta:
        unique_together = (('requestor','recipient'), )

    def __str__(self):
        return str(self.id)