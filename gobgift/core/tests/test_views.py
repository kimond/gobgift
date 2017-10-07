import pytest
from django.contrib.auth.models import AnonymousUser, User
from django.core.urlresolvers import reverse

from ..views import home, done

pytestmark = pytest.mark.django_db


class TestHome:
    @pytest.fixture()
    def user(self):
        return User.objects.create_user(username="Test", email="test@test.com", password="secret")

    def test_logged_user_is_redirected_to_done_page(self, rf, user):
        request = rf.get(reverse("home"))
        request.user = user
        response = home(request)
        assert response.status_code == 302