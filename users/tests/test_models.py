from django.test import TestCase
from users.models import User


class UserModelTest(TestCase):

    def test_modelCreation(self):
        user = User.objects.create(username='testUser',password='asdf',email='testemail@test.com')

        self.assertTrue(isinstance(user,User))

        #test __str__
        self.assertEquals(user.__str__(),user.username)