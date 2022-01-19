from django.urls import path
from django.conf.urls import include
from rest_framework import routers

from HallowSoup.views import TagViewSet, ArticleViewSet


router = routers.DefaultRouter()
router.register('tags', TagViewSet)
router.register('articles', ArticleViewSet)

urlpatterns = [ 
    path('', include(router.urls)),
]
