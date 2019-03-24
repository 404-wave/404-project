from django.test import TestCase
from users.models import  User
from django.urls import reverse
from django.contrib.auth.models import Permission
from friends import views

class FriendsViewTest(TestCase):
    url = reverse('friends')
    testuser=None

    def setUp(self):
        self.testuser = User.objects.create(username='t1')
        self.testuser.set_password('test')
        self.testuser.is_active = True
        self.testuser.save()
        
    def test_viewRenderNoLogin(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code,403,"Able to seee without logging in")

    def test_viewRenderLogin(self):
        login_url = reverse('login')
        login = self.client.post(login_url,{'username':'t1','password':'test'})
        self.assertTrue(login)

        response = self.client.get(self.url)
        self.assertEqual(response.status_code,200)
        

    