from django.test import TestCase
from users.models import  User, Node, NodeSetting
import requests
from requests.auth import HTTPBasicAuth

class AuthTest(TestCase):

    def test_auth(self):

        test_url = 'https://b71bb2e5.ngrok.io/service/posts/510cf811-9342-4d6d-beca-3a41d858762b/'
        headers = {
            'Accept':'application/json',
            # The UUID of the REQUESTING USER -- change as necessary
            'X-UUID': '4a47a810-4b00-4c59-8ec3-e0d4ac0b74fc'
        }
        r = requests.get(test_url, headers=headers, auth=HTTPBasicAuth('wave', 'wavepassword'))

        print()
        print()
        print("STATUS CODE: " + str(r.status_code))
        if r.status_code == 200:
            json = r.json() # Just to check that what was returned can be parsed
            print(r.content)
        print()
        print()
