from django.db import models

from users.models import User



class FollowManager(models.Manager):

    def get_friends(self, user):
        uid = user
        friends = set()
        follow_obj = Follow.objects.filter(Q(user2=uid)|Q(user1=uid))

        if follow_obj:
            for follow in follow_obj:
                if ((follow.user1==uid) & (follow.user2 not in friends)):
                    recip_object = Follow.objects.filter(user1=follow.user2,user2=follow.user1)
                    if recip_object:
                        user = User.objects.filter(id=follow.user2)
                        if user:    
                            user=user.get()
                        else:
                            user = get_user(follow.user2_server,follow.user2)
                            if user is None:
                                continue
                        friends.add(user)
                elif ((follow.user2==uid) & (follow.user1 not in friends)):
                    recip_object = Follow.objects.filter(user1=follow.user2,user2=follow.user1)
                    if recip_object:
                        user= User.objects.filter(id=follow.user1)
                        if user:
                            user=user.get()
                        else:
                            user= get_user(follow.user1_server,follow.user1)
                        friends.add(user)
        return friends

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
