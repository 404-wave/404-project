from django.db import models

from users.models import User


class Follow(models.Model):

    user1 = models.ForeignKey(User, related_name="follower", on_delete=models.CASCADE)
    user2 = models.ForeignKey(User, related_name="followee", on_delete=models.CASCADE)

    class Meta:
        unique_together = (('user1', 'user2'), )

    def __str__(self):
        return str(self.id)


class FriendRequest(models.Model):

    requestor = models.ForeignKey(User, related_name="requestor",on_delete=models.CASCADE)
    recipient = models.ForeignKey(User, related_name="recipient",on_delete=models.CASCADE)

    class Meta:
        unique_together = (('requestor','recipient'), )


    def __str__(self):
        return str(self.id)
