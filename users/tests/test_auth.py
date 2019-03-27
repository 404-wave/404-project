from django.test import TestCase
from users.models import  User, Node, NodeSetting
import requests
from requests.auth import HTTPBasicAuth

# TODO: We really should remove this test case. It's just here as a sample
class AuthTest(TestCase):

    def test_auth(self):

        test_url = 'https://cmput-404-proj-test.herokuapp.com/service/author/posts/'
        headers = {
            'Accept':'application/json',
            'X-UUID': '4a47a810-4b00-4c59-8ec3-e0d4ac0b74fc'
        }
        r = requests.get(test_url, headers=headers, auth=HTTPBasicAuth('local', 'strongpass'))

        print()
        print()
        print("STATUS CODE: " + str(r.status_code))
        if r.status_code == 200:
            json = r.json() # Just to check that what was returned can be parsed
            print(r.content)
        print()
        print()
