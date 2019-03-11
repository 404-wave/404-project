from django.test import TestCase
from .models import Post,PostManager
import datetime

class PostUnitTest(TestCase):
    person1 = None
    person2 = None
    person3 = None
    person4 = None
   
    def setUp(self):

        #create user objects
        self.person1 = User.objects.create(username="person1",password="test1")
        self.person2 = User.objects.create(username="person2",password="test2")
        self.person3 = User.objects.create(username="person3",password="test3")
        self.person4 = User.objects.create(username="person4",password="test4")
        self.person5 = User.objects.create(username="person5",password="test5")
        self.person6 = User.objects.create(username="person6",password="test6")
        self.person7 = User.objects.create(username="person7",password="test7")
    
        #create Follows for privacy

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


        #create posts
        
        #person1
        Post.objects.create(user=self.person1,content="hello friends",privacy=2,timestamp=datetime.datetime())
        Post.objects.create(user=self.person1,content="hello world",privacy=0,timestamp=datetime.datetime()-datetime.delta(days=30))
        Post.objects.create(user=self.person1,content="hello foafs",privacy=3,timestamp=datetime.datetime()-datetime.delta(days=183))
        Post.objects.create(user=self.person1,content="hello me",privacy=5,timestamp=datetime.datetime()-datetimes.delta(days=366))

        #person2
        Post.objects.create(user=self.person2,content="hello world",privacy=0, timestamp = datetime.datetime())

        #person3
        Post.objects.create(user=self.person3,content="hello server",privacy=4,timestamp = datetime.datetime()-datetime.delta(days=28))

        #person4
        Post.objects.create(user=self.person1,content="hello private",privacy=2, timestamp = datetime.datetime()-datetime.delta(days=181))
      
    def test_correctUser(self):
        #tests that the post belongs to the correct user

        post = Post.objects.filter(content="hello server")

        assertEqual(post.user.id,self.person3.id,"Incorrect UUID for the Post")
    def test_postGetter(self):
        #tests getter for Post
        
        posts = Post.objects.filter(user=self.person1)

        assertEqual(len(posts),4, "More/less posts retrieved than expected ")

        #testing for content
        

