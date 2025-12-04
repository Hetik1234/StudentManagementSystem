from django.test import TestCase
from django.contrib.auth.models import User

class TestAuth(TestCase):

    def test_user_signup(self):
        user = User.objects.create_user(username="testuser", password="pass12345")
        self.assertEqual(user.username, "testuser")

    def test_user_login(self):
        User.objects.create_user(username="loginuser", password="pass12345")
        login_success = self.client.login(username="loginuser", password="pass12345")
        self.assertTrue(login_success)
