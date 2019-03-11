from django.test import TestCase
from .models import User
from django.db.models import Q

class UserUnitTest(TestCase):
# Create your tests here.
    person1 = None
    person2 = None
    person3 = None
    person4 = None


    def setUp(self):
        self.person1 = User.objects.create(username="person1",bio="i am person1",
                                     github="p1git",is_active = True,is_admin=False)
        self.person2 = User.objects.create(username="person2",bio="i am person2",
                                     github="p2git",is_active = False,is_admin=False)
        self.person3 = User.objects.create(username="person3",bio="i am person3",
                                     github="p3git",is_active = True,is_admin=True)
        self.person4 = User.objects.create(username="person4",bio="i am person4",
                                     github="p4git",is_active = False,is_admin=True)

    
    def test_checkSameInfo(self):
        #checks if info is persistent through saving to DB
        user = User.objects.filter(username="person1")

        assertEquals(user.id,self.person1.id,"UUID is not the same")
        assertEquals(user.bio,self.person1.bio,"Bio is not the same")
        assertEquals(user.github,self.person1.github,"Bio is not the same")
        assertEquals(user.is_active,self.person1.is_active,"is_active is not the same")
        assertEquals(user.is_admin,self.person1.is_admin,"Admin status is not the same")

    def test_differentUUIDs(self):
        #checks that different UUID's are generated
        assertNotEqual(self.person1,self.person2)
        assertNotEqual(self.person3,self.person4)

        user = User.objects.filter(self.person3.id)
        assertTrue(len(user) == 1, "Filtering has 2 or more results")


    

