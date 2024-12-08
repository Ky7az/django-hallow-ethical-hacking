from django.test import TestCase

from HallowSoup.models import Article, Tag


class TagModelTestCase(TestCase):
    def setUp(self):
        Tag.objects.create(name='Tag', slug='tag')
        Article.objects.create(name='Article', slug='article', content='Content')

    def test_count_property(self):
        tag = Tag.objects.get(slug='tag')
        article = Article.objects.get(slug='article')
        article.tags.add(tag)
        self.assertEqual(tag.count, article.tags.count())

    def test_string_method(self):
        tag = Tag.objects.get(slug='tag')
        self.assertEqual(str(tag), f'{tag.name}')


class ArticleModelTestCase(TestCase):
    def setUp(self):
        Article.objects.create(name='Article', slug='article', content='Content')

    def test_string_method(self):
        article = Article.objects.get(slug='article')
        self.assertEqual(str(article), f'{article.name}')
