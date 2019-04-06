from django.db import models

from users.models import User



class FollowManager(models.Manager):

    def get_friends(self, user):
        pass

class Follow(models.Model):
    #user1 is follower , user2 is followee
    user1 = models.UUIDField()
    user1_server = models.CharField(max_length=200,default="000")
    user2 = models.UUIDField()
    user2_server = models.CharField(max_length=200,default="000")

    class Meta:
        unique_together = (('user1', 'user2'), )

    def __str__(self):
        return str(self.id)

    


class FriendRequest(models.Model):

    requestor = models.UUIDField()
    requestor_server = models.CharField(max_length=200,default="000")
    recipient = models.UUIDField()
    recipient_server = models.CharField(max_length=200,default="000")

    class Meta:
        unique_together = (('requestor','recipient'), )

    def __str__(self):
        return str(self.id)
