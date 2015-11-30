from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.decorators import detail_route, list_route
from rest_framework.response import Response
from gobgift_api.serializers import ListeSerializer, GiftSerializer
from gobgift.models import Liste, Gift


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
    A viewset for viewing and editing list instances.
    """
    serializer_class = GiftSerializer
    queryset = Gift.objects.all()