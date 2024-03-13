from django.urls import include, path
from rest_framework import routers

from HallowWatch.views import (
    ContentViewSet,
    FeedViewSet,
    SourceViewSet,
    TagViewSet
)

router = routers.DefaultRouter()
router.register('tags', TagViewSet)
router.register('sources', SourceViewSet)
router.register('feeds', FeedViewSet)
router.register('contents', ContentViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
