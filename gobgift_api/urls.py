from django.conf.urls import url, include
from rest_framework import routers
from gobgift_api.views import (ListeViewSet, GiftViewSet, ListGroupViewSet,
                               CommentViewSet, ListGroupUserViewSet,
                               ListGiftList, ListGroupList)

router = routers.DefaultRouter()
router.register(r'lists', ListeViewSet)
router.register(r'gifts', GiftViewSet)
router.register(r'listgroups', ListGroupViewSet)
router.register(r'listgroupusers', ListGroupUserViewSet)
router.register(r'comments', CommentViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
  url(r'', include(router.urls)),
  url(r'^lists/(?P<pk>\d+)/gifts', ListGiftList.as_view(),
      name='list-gift-list'),
  url(r'^listgroups/(?P<pk>\d+)/lists', ListGroupList.as_view(),
      name='listgroup-list-list')
]
