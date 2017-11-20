from rest_framework import serializers

from gobgift.core.serializers import UserSerializer
from gobgift.groups.models import ListGroup, ListGroupUser


class ListGroupSerializer(serializers.ModelSerializer):
    owner = UserSerializer(read_only=True)

    class Meta:
        model = ListGroup
        fields = ('id', 'name', 'owner')


class ListGroupUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = ListGroupUser
        fields = ('group', 'user', 'is_admin')
