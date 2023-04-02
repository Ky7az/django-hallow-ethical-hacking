from django.urls import path
from django.conf.urls import include
from rest_framework import routers

from HallowWatch.views import TagViewSet, SourceViewSet, FeedViewSet, ContentViewSet


router = routers.DefaultRouter()
router.register('tags', TagViewSet)
router.register('sources', SourceViewSet)
router.register('feeds', FeedViewSet)
router.register('contents', ContentViewSet)

urlpatterns = [ 
    path('', include(router.urls)),
]
