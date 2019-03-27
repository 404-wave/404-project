from django.test import TestCase
from users.models import  User, Node, NodeSetting
import requests
from requests.auth import HTTPBasicAuth


class AuthTest(TestCase):

    def test_auth(self):
        # 4a47a810-4b00-4c59-8ec3-e0d4ac0b74fc
        #headers = {'X-UUID': self.context.get('requestor')}
        user = Node.objects.create(username='local',password='strongpass', host='https://cmput-404-proj-test.herokuapp.com')

        for node in Node.objects.all():
            url_to_node = node.host + '/posts/'
            print(url_to_node)
            r = requests.get(node.host, auth=HTTPBasicAuth(node.username, node.password))

            print()
            print()
            print("STATUS CODE: " + str(r.status_code))
            if r.status_code == 200:
                print(r.content)
            print()
            print()
