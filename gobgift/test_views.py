from django.contrib.auth.models import AnonymousUser, User
from django.core.urlresolvers import reverse
from django.test import RequestFactory
from django.test import TestCase

from .views import home, done


class HomeTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username="Test", email="test@test.com", password="secret")

    def test_anonymous_user(self):
        request = self.factory.get(reverse("home"))
        request.user = AnonymousUser()
        response = home(request)
        self.assertEquals(response.status_code, 200)

    def test_logged_user(self):
        request = self.factory.get(reverse("home"))
        request.user = self.user
        response = home(request)
        self.assertEquals(response.status_code, 302)

    def test_done_logged(self):
        request = self.factory.get(reverse("done"))
        request.user = self.user
        response = done(request)
        self.assertEquals(response.status_code, 200)
