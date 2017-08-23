from rest_framework import serializers

from gobgift.groups.models import ListGroup, ListGroupUser


class ListGroupSerializer(serializers.ModelSerializer):
    owner = serializers.StringRelatedField()

    class Meta:
        model = ListGroup
        fields = ('id', 'name', 'owner')


class ListGroupUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = ListGroupUser
        fields = ('group', 'user', 'is_admin')
