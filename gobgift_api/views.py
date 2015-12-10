from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.decorators import detail_route, list_route
from rest_framework.response import Response
from gobgift_api.serializers import (ListeSerializer, GiftSerializer, 
                                     ListGroupSerializer, CommentSerializer,
                                     ListGroupUserSerializer)
from gobgift.models import Liste, Gift, ListGroup, ListGroupUser, Comment


class ListGroupViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing listgroup instances
    """
    serializer_class = ListGroupSerializer
    queryset = ListGroup.objects.none()
    

class ListGroupUserViewSet(viewsets.ModelViewSet):
    serializer_class = ListGroupUserSerializer()
    queryset = ListGroupUser.objects.none()
    

class ListeViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing list instances.
    """
    serializer_class = ListeSerializer
    queryset = Liste.objects.all()
    
    @list_route()
    def my_lists(self, request):
        my_lists = Liste.objects.all()

        serializer = self.get_serializer(my_lists, many=True)
        return Response(serializer.data)


class GiftViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing gift instances.
    """
    serializer_class = GiftSerializer
    queryset = Gift.objects.none()
    
    
class CommentViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing comment instances.
    """
    serializer_class = CommentSerializer
    queryset = Comment.objects.none()