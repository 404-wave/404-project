from django.test import TestCase
from users.models import  User
from django.urls import reverse
from users import views 
from users.forms import UserCreationForm

class UserRegistrationViewTest(TestCase):
    url = reverse('register')

    def test_viewRender(self):
        #should pass
        response = self.client.get(self.url)
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response, 'registration/register.html')

    def test_blankReg(self):
        #should pass
        self.client.post(self.url,{})
        self.assertFalse(User.objects.filter(username='').exists(),"Blank Registration created user")

    def test_validReg(self):
        
        self.client.post(self.url, {'username':'testValid','email':'test@test.com','password1':'Testcasepwd','password2':'Testcasepwd'},HTTP_HOST='example.com')
        self.assertTrue(User.objects.filter(username='testValid').exists(),'Valid Registration user was not created')
   
    def test_invalidReg(self):
        #invalid email
        self.client.post(self.url,{'username':'test','email':'123@123'
                                            ,'password1':'Testcasepwd','password2':'Testcasepwd'})
        self.assertFalse(User.objects.filter(username='test').exists(),"invalid email user was created")

        #passwords don't match
        self.client.post(self.url,{'username':'test2','email':'123@123.com',
                                            'password1':'Testcasepwddd','password2':'Testcasepwd'})
        self.assertFalse(User.objects.filter(username='test2').exists(),"Password mismatch user was created")
        