from collections import OrderedDict

from django.test import TestCase
from django.utils.timezone import localtime

from HallowSoup.models import Article, Tag
from HallowSoup.serializers import ArticleSerializer, TagSerializer


class TagSerializerTestCase(TestCase):

    def test_tag(self):
        tag = Tag.objects.create(name='Tag', slug='tag')
        expected = {
            'id': tag.id,
            'name': 'Tag',
            'slug': 'tag',
            'count': 0
        }
        serializer = TagSerializer(tag)
        self.assertEquals(serializer.data, expected)


class ArticleSerializerTestCase(TestCase):

    def test_article(self):
        article = Article.objects.create(name='Article', slug='article', content='Content')
        tag = Tag.objects.create(name='Tag', slug='tag')
        article.tags.add(tag)
        expected = {
            'id': article.id,
            'name': 'Article',
            'slug': 'article',
            'content': 'Content',
            'tags': [OrderedDict([('id', tag.id), ('name', 'Tag'), ('slug', 'tag'), ('count', 1)])],
            'bookmarked': False,
            'create_date': localtime(article.create_date).isoformat().replace('+00:00', 'Z'),
            'write_date': localtime(article.write_date).isoformat().replace('+00:00', 'Z'),
            'active': True
        }
        serializer = ArticleSerializer(article)
        self.assertEquals(serializer.data, expected)
