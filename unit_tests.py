import json
import random
import uuid
import unittest
from app import app


class UserTest(unittest.TestCase):

    def setUp(self):
        self.name = f"Your name - {uuid.uuid4()}"
        self.username = f"username{random.randint(0, 9999)}"
        self.email = f"username{random.randint(0, 9999)}@username.com.br"
        self.level = 3
        self.token = None

    def perform_login(self):
        with app.test_client() as tester:
            response = tester.post("http://localhost:5000/api/session/perform",
                                   headers={
                                       "Content-Type": "application/json"},
                                   data=json.dumps({"username": 'developer', 'password': "developer"})).get_json()
        self.token = response['token']

    def revoke_login(self):
        with app.test_client() as tester:
            tester.delete("http://localhost:5000/api/session/revoke",
                          headers={
                              "Content-Type": "application/json",
                              "Authorization": f"Bearer {self.token}"}
                          )

    def test_perform_login(self):

        with app.test_client() as tester:
            response = tester.post("http://localhost:5000/api/session/perform",
                                   headers={
                                       "Content-Type": "application/json"},
                                   data=json.dumps({"username": 'developer', 'password': "developer"}))

            self.assertEqual(200, response.status_code)
            response = response.get_json()
            self.assertIsNotNone(response)
            self.assertIsNotNone(response['token'])
            self.token = response['token']
            self.assertEqual(
                response['message'], "User successfully logged in.")

    def test_revoke_login(self):

        self.perform_login()

        with app.test_client() as tester:
            response = tester.delete("http://localhost:5000/api/session/revoke",
                                     headers={
                                         "Content-Type": "application/json",
                                         "Authorization": f"Bearer {self.token}"}
                                     )
            self.assertEqual(200, response.status_code)
            response = response.get_json()
            self.assertEqual("Token revoked.", response['message'])

    def test_revoke_revoked_token(self):

        self.perform_login()

        self.revoke_login()

        with app.test_client() as tester:
            response = tester.delete("http://localhost:5000/api/session/revoke",
                                     headers={
                                         "Content-Type": "application/json",
                                         "Authorization": f"Bearer {self.token}"}
                                     )
            self.assertEqual(401, response.status_code)
            response = response.get_json()
            self.assertEqual("You are not logged in.", response['message'])

# verificar no log de coverage cenarios restantes


if __name__ == '__main__':
    unittest.main()
