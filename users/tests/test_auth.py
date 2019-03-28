from django.test import TestCase
from users.models import  User, Node, NodeSetting
import requests
from requests.auth import HTTPBasicAuth

class AuthTest(TestCase):

    def test_auth(self):

        test_url = 'https://cmput-404-proj-test.herokuapp.com/service/posts/'
        headers = {
            'Accept':'application/json',
            # The UUID of the REQUESTING USER -- change as necessary
            'X-UUID': '4a47a810-4b00-4c59-8ec3-e0d4ac0b74fc'
        }
        #r = requests.get(test_url, headers=headers, auth=HTTPBasicAuth('local', 'localpassword'))



        # url = node.host + "/service/posts/"
        test_url = 'https://cmput-404-proj-test.herokuapp.com/service/posts/{0}'.format(str('2161facd-48c4-4f53-8006-52cbc6cec971')) + "/"

        #print("This is my request id", request.user.id)
        print("Here is the url: " + test_url)

        # headers = {
        #     'Accept': 'application/json',
        #     'X-UUID': str(request.user.id)
        # }
        # response = requests.get(url, headers=headers, auth=HTTPBasicAuth(
        #     str(node.username), str(node.password)))

        headers = {
            'Accept': 'application/json',
            'X-UUID': '2161facd-48c4-4f53-8006-52cbc6cec971'
        }
        r = requests.get(test_url, headers=headers,
                                auth=HTTPBasicAuth('local', 'localpassword'))

        print()
        print()
        print("STATUS CODE: " + str(r.status_code))
        if r.status_code == 200:
            json = r.json() # Just to check that what was returned can be parsed
            print(r.content)
        print()
        print()
