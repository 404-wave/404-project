from django.test import TestCase
from users.models import  User
from django.urls import reverse
from core import views

class CoreViewsTesting(TestCase):
    myprofile_url = reverse('my_profile')
    friends_url = reverse('my_friends')


    def setUp(self):
        self.testuser = User.objects.create(username='t1')
        self.testuser.set_password('test')
        self.testuser.is_active = True
        self.testuser.save()


    def test_myProfileNoLogin(self):
        response = self.client.get(self.myprofile_url)

        self.assertEqual(response.status_code,302,"Allowed to view my profile without logging in")
    
    def test_myProfileLogin(self):
        login_url = reverse('login')
        login = self.client.post(login_url,{'username':'t1','password':'test'})
        self.assertTrue(login)

        response = self.client.post(self.myprofile_url)
        self.assertEqual(response.status_code,200, "Couldn't see my profile even if logged in")


    def test_viewFriendsNoLogin(self):
        response = self.client.get(self.friends_url)

        self.assertEqual(response.status_code,403,"Allowed to see friends without logging in")
        self.assertTemplateNotUsed(response,'friends.html')

    def test_viewFriendsLogin(self):
        login_url = reverse('login')
        login = self.client.post(login_url,{'username':'t1','password':'test'})
        self.assertTrue(login)
        
        response = self.client.get(self.friends_url)
        self.assertEqual(response.status_code,200,"Logged in but can't see friends")
        self.assertTemplateUsed(response,'friends.html')


