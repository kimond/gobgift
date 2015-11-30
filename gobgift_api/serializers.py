from rest_framework import serializers
from gobgift.models import Liste, ListGroup, ListGroupUser, Gift


class ListeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Liste
        fields = ('id', 'owner', 'name', 'groups')
        
        
class ListGroupSerializer(serializers.ModelSerializer):
    class Meta:
      model = ListGroup
      fields = ('name', 'owner')
        
        
class ListGroupUserSerializer(serializers.ModelSerializer):
    class Meta:
      model = ListGroupUser
      fields = ('group', 'user', 'is_admin')
        
        
class GiftSerializer(serializers.ModelSerializer):
    class Meta:
      model = Gift
      fields = ('liste', 'name', 'photo', 'description',
                'price', 'siteweb', 'store', 'purchased')