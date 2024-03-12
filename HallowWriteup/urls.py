from django.urls import include
from django.urls import path
from rest_framework import routers

from HallowWriteup.views import ReportViewSet, TagViewSet, WebsiteViewSet

router = routers.DefaultRouter()
router.register('tags', TagViewSet)
router.register('websites', WebsiteViewSet)
router.register('reports', ReportViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
