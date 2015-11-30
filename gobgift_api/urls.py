from django.conf.urls import url, include
from rest_framework import routers
from gobgift_api.views import ListeViewSet, GiftViewSet

router = routers.DefaultRouter()
router.register(r'lists', ListeViewSet)
router.register(r'gifts', GiftViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
  url(r'', include(router.urls)),
]