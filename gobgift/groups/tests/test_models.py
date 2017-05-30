from django.contrib.auth.models import User
from ..models import ListGroup, ListGroupUser


class ListGroupTest:
    def test_string_representation(self):
        list_group = ListGroup(name="Test")
        assert str(list_group) == list_group.name


class ListGroupUserTest:
    def test_string_representation(self):
        user = User.objects.create_user(username="johnd", first_name="John", email="test@test.com", last_name="Deer")
        list_group_user = ListGroupUser(user=user)
        string_representation = user.first_name + " " + user.last_name
        assert str(list_group_user) == string_representation
