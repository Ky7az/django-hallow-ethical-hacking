from django_filters.rest_framework import (BooleanFilter, CharFilter,
                                           ChoiceFilter, DjangoFilterBackend,
                                           FilterSet,
                                           ModelMultipleChoiceFilter)
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated

from HallowWatch.models import Content, Feed, Source, Tag
from HallowWatch.serializers import (ContentSerializer, FeedSerializer,
                                     SourceSerializer, TagSerializer)


class TagViewSet(viewsets.ModelViewSet):

    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    lookup_field = 'slug'


class SourceViewSet(viewsets.ModelViewSet):

    queryset = Source.objects.all()
    serializer_class = SourceSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    lookup_field = 'slug'


class FeedViewSet(viewsets.ModelViewSet):

    queryset = Feed.objects.all()
    serializer_class = FeedSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    lookup_field = 'id'


class ContentFilter(FilterSet):

    title = CharFilter(field_name='title', lookup_expr='icontains')
    tag = ModelMultipleChoiceFilter(
        field_name='tag__slug',
        to_field_name='slug',
        queryset=Tag.objects.all()
    )
    source_type = ChoiceFilter(field_name='source__source_type', choices=Source.SOURCE_TYPES)
    viewed = BooleanFilter(field_name='viewed')
    bookmarked = BooleanFilter(field_name='bookmarked')

    class Meta:
        model = Content
        fields = ['title', 'tag', 'source_type', 'viewed', 'bookmarked']


class ContentPagination(PageNumberPagination):

    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 20
    page_query_param = 'page'


class ContentViewSet(viewsets.ModelViewSet):

    queryset = Content.objects.all()
    serializer_class = ContentSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    filter_backends = [DjangoFilterBackend]
    filterset_class = ContentFilter
    pagination_class = ContentPagination
    lookup_field = 'id'
