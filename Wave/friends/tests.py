from django.test import TestCase
from .models import Follow
from users.models import User
from django.db.models import Q
from django.db import connection


#Tests if follow outputs the correct users for "followed" and "following"
class FollowTestCase(TestCase):
    person1 = None
    person2 = None
    person3 = None
    person4 = None
    person5 = None
    person6 = None
    person7 = None


    
    def setUp(self):
        #create user objects
        self.person1 = User.objects.create(username="person1",password="test1")
        self.person2 = User.objects.create(username="person2",password="test2")
        self.person3 = User.objects.create(username="person3",password="test3")
        self.person4 = User.objects.create(username="person4",password="test4")
        self.person5 = User.objects.create(username="person5",password="test5")
        self.person6 = User.objects.create(username="person6",password="test6")
        self.person7 = User.objects.create(username="person7",password="test7")

        #create Follows

        #p1 follows: 2,3,4
        #p2 follows: 3
        #p3 follows: 2,4
        #p4 follows: 3,7
        #p5 follows: no one
        #p6 follows: 7
        #p7 follows: 6,4

        Follow.objects.create( user1 = self.person1,user2=self.person2)
        Follow.objects.create(user1=self.person1,user2=self.person3)
        Follow.objects.create(user1= self.person3,user2=self.person2)
        Follow.objects.create(user1=self.person2,user2=self.person3)
        Follow.objects.create(user1=self.person3,user2=self.person4)
        Follow.objects.create(user1=self.person4,user2=self.person3)
        Follow.objects.create(user1=self.person6,user2=self.person7)
        Follow.objects.create(user1=self.person4,user2=self.person7)
        Follow.objects.create(user1=self.person7,user2=self.person6)
        Follow.objects.create(user1=self.person7,user2=self.person4)
        Follow.objects.create(user1=self.person1,user2=self.person4)

        

    #TODO change to UUID after PR is merged
    def test_followeesCorrect(self):
        #tests if the follower has the correct followee's
        queryset = Follow.objects.filter(user1=self.person1)
        expected1= "person2"
        expected2 = "person3"
        expected3 = "person4"
        notexpected = "person5"
        
        for person in queryset:
            follower = person.user2.username
            self.assertNotEqual(follower,notexpected)
            correct = False
            if follower == expected1 or follower == expected2 or follower==expected3:
                correct = True
            self.assertTrue(correct, "Follower does not have correct followees")
   
    #TODO change to UUID after PR is merged
    def test_followersCorrect(self):
        #tests if the followees have the correct follower's
        follower_objs = Follow.objects.filter(user2=self.person3)

        expected1 = 'person1'
        expected2 = 'person2'
        expected3 = 'person4'
        notexpected= 'person 6'
        for person in follower_objs:
            follower = person.user1.username
            self.assertNotEqual(follower,notexpected)
            if follower == expected1 or follower == expected2 or follower==expected3:
                correct = True
            self.assertTrue(correct, "Followee does not have correct followers")

    def test_correctImmediateFriends(self):
        #tests for immediate friends, aka user x and user y follow each other
        friends = self.queryFriends(self.person3)
        expected = {self.person2,self.person4}
        self.assertEqual(friends,expected,"Immediate friends are not correct")

    def test_falsePositiveImmediateFriends(self):
        #tests to make sure that no false positives appear
        friends = self.queryFriends(self.person5)
        expected = set() #person 5 has no friends
        self.assertEqual(friends,expected,"False positive for immediate friends")
    
    def test_correctMutuals(self):
        #tests if the user has the correct set of mutual friends
        #Assumes that that the users are already following each other
        #does not include immediate friends       
        #Testing for person4
        #Expected outcome: person2, person6
        mutuals = set()
        target = self.person4
        friends = self.queryFriends(target)      
        for friend in friends:
            fof = self.queryFriends(friend)
            for person in fof:
                mutuals.add(person)
        mutuals.remove(target)
        expected = {self.person2,self.person6}

        self.assertEqual(mutuals,expected, "Incorrect mutual friends")

    def test_falsePositiveMutuals(self):
        #tests for false positives for mutual friends
        mutuals = set()
        target = self.person1
        friends = self.queryFriends(target)
        for friend in friends:
            fof = self.queryFriends(friend)
            for person in fof:
                mutuals.add(person)
        expected = set() #person1 only follows, so empty set

        self.assertEqual(mutuals,expected, "False positive for mutual friends")
    
    def queryFriends(self,target):
        friendsOfTarget = set()
        timesAppeared = []
        person_query = Follow.objects.filter(Q(user1=target) | Q(user2=target))
        for followobj in person_query:
            if followobj.user1 == target :
                if followobj.user2 in timesAppeared:
                    friendsOfTarget.add(followobj.user2)
                else:
                    timesAppeared.append(followobj.user2)
            elif followobj.user2 == target:
                if followobj.user1 in timesAppeared:
                    friendsOfTarget.add(followobj.user1)
                else:
                    timesAppeared.append(followobj.user1)
        
        return friendsOfTarget
