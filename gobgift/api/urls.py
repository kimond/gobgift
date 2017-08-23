from django.conf.urls import url, include
from rest_framework import routers

from gobgift.api.views import (WishlistViewSet, GiftViewSet, ListGroupViewSet,
                               CommentViewSet, ListGroupUserViewSet,
                               ListGiftList, ListGroupList, GiftCommentList)

router = routers.DefaultRouter()
router.register(r'lists', WishlistViewSet)
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
      name='listgroup-list-list'),
  url(r'^gifts/(?P<pk>\d+)/comments', GiftCommentList.as_view(),
      name='gift-comment-list')
]
