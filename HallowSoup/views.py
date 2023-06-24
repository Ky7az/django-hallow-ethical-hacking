from django.db.models import Q
from django_filters.rest_framework import (BooleanFilter, CharFilter,
                                           DjangoFilterBackend, FilterSet,
                                           ModelMultipleChoiceFilter)
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated

from HallowSoup.models import Article, Tag
from HallowSoup.serializers import ArticleSerializer, TagSerializer


class TagViewSet(viewsets.ModelViewSet):

    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAuthenticated, )
    lookup_field = 'slug'


class ArticleFilter(FilterSet):

    name_or_content = CharFilter(method='filter_name_or_content')
    tags = ModelMultipleChoiceFilter(
        field_name='tags__slug',
        to_field_name='slug',
        queryset=Tag.objects.all()
    )
    bookmarked = BooleanFilter(field_name='bookmarked')

    def filter_name_or_content(self, queryset, name, value):
        return queryset.filter(Q(name__icontains=value) | Q(content__icontains=value))

    class Meta:
        model = Article
        fields = ['name_or_content', 'tags', 'bookmarked']


class ArticlePagination(PageNumberPagination):

    page_size = 18
    page_size_query_param = 'page_size'
    max_page_size = 18
    page_query_param = 'page'


class ArticleViewSet(viewsets.ModelViewSet):

    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAuthenticated, )
    filter_backends = [DjangoFilterBackend]
    filterset_class = ArticleFilter
    pagination_class = ArticlePagination
    lookup_field = 'slug'
