from django.test import SimpleTestCase
from django.urls import reverse, resolve
from smsapp import views

class TestUrls(SimpleTestCase):

    def test_home_url(self):
        url = reverse('home')
        self.assertEqual(resolve(url).func, views.home)
