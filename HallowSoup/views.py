from django.contrib.auth.models import User
from django.db.models import Q
from rest_framework import viewsets, generics
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from django_filters.rest_framework import DjangoFilterBackend, FilterSet, CharFilter, ModelMultipleChoiceFilter

from HallowSoup.models import Tag, Article
from HallowSoup.serializers import TagSerializer, ArticleSerializer, UserSerializer


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    # authentication_classes = (TokenAuthentication, )
    # permission_classes = (IsAuthenticated, )
    lookup_field = 'slug'

class ArticleFilter(FilterSet):
    name_or_content = CharFilter(method='filter_name_or_content')
    tags = ModelMultipleChoiceFilter(
        field_name='tags__slug',
        to_field_name='slug',
        queryset=Tag.objects.all()
    )

    def filter_name_or_content(self, queryset, name, value):
        return queryset.filter(Q(name__icontains=value) | Q(content__icontains=value))

    class Meta:
        model = Article
        fields = ['name_or_content', 'tags']

class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    # authentication_classes = (TokenAuthentication, )
    # permission_classes = (IsAuthenticated, )
    filter_backends = [DjangoFilterBackend]
    filterset_class = ArticleFilter
    lookup_field = 'slug'

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny, )
