from django.urls import path
from django.conf.urls import include
from rest_framework import routers

from HallowWriteup.views import TagViewSet, WebsiteViewSet, ReportViewSet


router = routers.DefaultRouter()
router.register('tags', TagViewSet)
router.register('websites', WebsiteViewSet)
router.register('reports', ReportViewSet)

urlpatterns = [ 
    path('', include(router.urls)),
]
