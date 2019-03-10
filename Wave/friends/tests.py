from django.test import TestCase
from .models import Follow
from users.models import User

#Tests if follow outputs the correct users for "followed" and "following"
class FollowTestCase(TestCase):
    person1 = None
    person2 = None
    person3 = None
    
    def setUp(self):
        #create user objects
        self.person1 = User.objects.create(username="person1",password="test1")
        self.person2 = User.objects.create(username="person2",password="test2")
        self.person3 = User.objects.create(username="person3",password="test3")
        
        #create Follows
        Follow.objects.create( user1 = self.person1,user2=self.person2)
        Follow.objects.create(user1=self.person1,user2=self.person3)
        Follow.objects.create(user1= self.person3,user2=self.person2)

    #TODO change to UUID after PR is merged
    def test_followeesCorrect(self):
        #tests if the follower has the correct followee's
        queryset = Follow.objects.filter(user1=self.person1)
        expected1= "person2"
        expected2 = "person3"
        for person in queryset:
            follower = person.user2.username
            correct = False
            if follower == expected1 or follower == expected2:
                correct = True
            self.assertTrue(correct, "Follower does not have correct followees")

    
