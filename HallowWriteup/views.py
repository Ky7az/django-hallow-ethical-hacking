from django.db.models import Q
from django_filters.rest_framework import (CharFilter, DjangoFilterBackend,
                                           FilterSet,
                                           ModelMultipleChoiceFilter,
                                           MultipleChoiceFilter)
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated

from HallowWriteup.models import Report, Tag, Website
from HallowWriteup.serializers import (ReportSerializer, TagSerializer,
                                       WebsiteSerializer)


class TagViewSet(viewsets.ModelViewSet):

    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    lookup_field = 'slug'


class WebsiteViewSet(viewsets.ModelViewSet):

    queryset = Website.objects.all()
    serializer_class = WebsiteSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    lookup_field = 'slug'


class ReportFilter(FilterSet):

    name_or_content = CharFilter(method='filter_name_or_content')
    tags = ModelMultipleChoiceFilter(
        field_name='tags__slug',
        to_field_name='slug',
        queryset=Tag.objects.all()
    )
    website = ModelMultipleChoiceFilter(
        field_name='website__slug',
        to_field_name='slug',
        queryset=Website.objects.all()
    )
    task_type = MultipleChoiceFilter(choices=Report.TASK_TYPES)
    task_platform = MultipleChoiceFilter(choices=Report.TASK_PLATFORMS)

    def filter_name_or_content(self, queryset, name, value):
        return queryset.filter(Q(name__icontains=value) | Q(content__icontains=value))

    class Meta:
        model = Report
        fields = ['name_or_content', 'tags', 'website', 'task_type', 'task_platform']


class ReportPagination(PageNumberPagination):

    page_size = 18
    page_size_query_param = 'page_size'
    max_page_size = 18
    page_query_param = 'page'


class ReportViewSet(viewsets.ModelViewSet):

    queryset = Report.objects.all()
    serializer_class = ReportSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    filter_backends = [DjangoFilterBackend]
    filterset_class = ReportFilter
    pagination_class = ReportPagination
    lookup_field = 'slug'
