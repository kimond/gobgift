from rest_framework import serializers
from gobgift.models import Liste, ListGroup, ListGroupUser, Gift, Comment


class ListeSerializer(serializers.ModelSerializer):
    owner = serializers.StringRelatedField()

    class Meta:
        model = Liste
        fields = ('id', 'owner', 'name', 'groups')


class ListGroupSerializer(serializers.ModelSerializer):
    owner = serializers.StringRelatedField()

    class Meta:
        model = ListGroup
        fields = ('id', 'name', 'owner')


class ListGroupUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = ListGroupUser
        fields = ('group', 'user', 'is_admin')


class GiftSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gift
        fields = ('id', 'liste', 'name', 'photo', 'description',
                  'price', 'siteweb', 'store', 'purchased')


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('gift', 'user', 'text', 'datetime')
