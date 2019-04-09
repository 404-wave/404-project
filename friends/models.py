from django.db import models
from users.models import User
from django.db.models import Q



class FollowManager(models.Manager):

    def get_friends(self, user):
        uid = user.id
        follow_obj = Follow.objects.filter(Q(user2=uid)|Q(user1=uid))
        friends = list()

        if follow_obj:
            for follow in follow_obj:
                recip_object1= Follow.objects.filter(user1=str(uid),user2=follow.user1)
                recip_object2= Follow.objects.filter(user1=follow.user1,user2=str(uid))
                if (recip_object1 and recip_object2):
                    if (recip_object1[0].user1 == recip_object2[0].user2 and recip_object1[0].user2 == recip_object2[0].user1):
                        friends.append([recip_object2[0].user1,recip_object2[0].user1_server])
        friend2 = (item[1]+'author/'+str(item[0]) for item in friends)
        return(list(friend2))

    def get_friends_id(self, uuid):
        uid = uuid
        follow_obj = Follow.objects.filter(Q(user2=uid)|Q(user1=uid))
        friends = list()

        if follow_obj:
            for follow in follow_obj:
                recip_object1= Follow.objects.filter(user1=str(uid),user2=follow.user1)
                recip_object2= Follow.objects.filter(user1=follow.user1,user2=str(uid))
                if (recip_object1 and recip_object2):
                    if (recip_object1[0].user1 == recip_object2[0].user2 and recip_object1[0].user2 == recip_object2[0].user1):
                        friends.append([recip_object2[0].user1,recip_object2[0].user1_server])
        friend2 = (item[1]+'author/'+str(item[0]) for item in friends)
        return(list(friend2))

class Follow(models.Model):
    #user1 is follower , user2 is followee
    user1 = models.UUIDField()
    user1_server = models.CharField(max_length=200,default="000", unique=False)
    user2 = models.UUIDField()
    user2_server = models.CharField(max_length=200,default="000", unique=False)

    class Meta:
        unique_together = (('user1', 'user2'), )

    def __str__(self):
        return str(self.id)
        
class FriendRequestManager(models.Manager):

    def get_friend_requests(self, user):
        uid = user.id
        friend_obj = FriendRequest.objects.filter(Q(recipient=uid))
        friend2 = (item.requestor_server+'author/'+str(item.requestor) for item in friend_obj)
        return(list(friend2))

class FriendRequest(models.Model):

    requestor = models.UUIDField()
    requestor_server = models.CharField(max_length=200,default="000", unique=False)
    recipient = models.UUIDField()
    recipient_server = models.CharField(max_length=200,default="000", unique=False)

    class Meta:
        unique_together = (('requestor','recipient'), )

    def __str__(self):
        return str(self.id)
