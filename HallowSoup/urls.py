from django.urls import include
from django.urls import path
from rest_framework import routers

from HallowSoup.views import ArticleViewSet, TagViewSet

router = routers.DefaultRouter()
router.register('tags', TagViewSet)
router.register('articles', ArticleViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
