from django.test import TestCase
from users.models import User
from users.forms import UserCreationForm

class UserFormTest(TestCase):

    def test_valid_all(self):
        #tests for valid all inputs
        data = {'username': 'validNamee','email':'test@usertest.com','first_name':'valid','last_name':'user','password1':'Testcasepwd','password2':'Testcasepwd'}
        form = UserCreationForm(data=data)
        self.assertTrue(form.is_valid())

    def test_valid_noFirstLast(self):
        #tests for valid -- no first and last
        data = {'username': 'validName','email':'test@usertest.com','password1':'Testcasepwd','password2':'Testcasepwd'}
        form = UserCreationForm(data=data)
        self.assertTrue(form.is_valid())


    
    def test_invalid_noUser(self):
        #test for no username
        data = {'first_name':'valid','last_name':'user','password1':'Testcasepwd','password2':'Testcasepwd','email':'test@usertest.com'}
        form = UserCreationForm(data)
        self.assertFalse(form.is_valid())

    def test_invalid_noPwd(self):
        #test for no password
        data = {'first_name':'valid','last_name':'user','email':'test@usertest.com'}
        form = UserCreationForm(data)
        self.assertFalse(form.is_valid())

    def test_invalid_noEmail(self):
        #test for no email
        data = {'first_name':'valid','last_name':'user','password1':'Testcasepwd','password2':'Testcasepwd'}
        form = UserCreationForm(data)
        self.assertFalse(form.is_valid())


