import pytest
from django.contrib.auth.models import User
from django.test.client import Client


@pytest.fixture()
def logged_client(db) -> Client:
    """A Django test client logged in as an regular user."""
    user = User.objects.create(username='test', password='test_password')
    client = Client()
    client.login(username=user.username, password='test_password')
    return client
