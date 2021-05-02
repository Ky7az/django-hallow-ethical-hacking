from django.urls import path
from django.conf.urls import include
from rest_framework import routers

from HallowSoup.views import TagViewSet, ArticleViewSet, UserViewSet


router = routers.DefaultRouter()
router.register('tags', TagViewSet)
router.register('articles', ArticleViewSet)
router.register('users', UserViewSet)

urlpatterns = [ 
    path('', include(router.urls)),
]
