from collections import OrderedDict

from django.test import TestCase
from django.utils.timezone import localtime

from HallowWatch.models import Content, Feed, Source, Tag
from HallowWatch.serializers import (
    ContentSerializer,
    FeedSerializer,
    SourceSerializer,
    TagSerializer
)


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


class SourceSerializerTestCase(TestCase):

    def test_source(self):
        source = Source.objects.create(name='Source', slug='source', source_type='security', url='www.source.tld')
        expected = {
            'id': source.id,
            'name': 'Source',
            'slug': 'source',
            'source_type': 'security',
            'source_type_display': 'Security',
            'url': 'www.source.tld'
        }
        serializer = SourceSerializer(source)
        self.assertEquals(serializer.data, expected)


class FeedSerializerTestCase(TestCase):

    def test_feed(self):
        source = Source.objects.create(name='Source', slug='source', source_type='security', url='www.source.tld')
        feed = Feed.objects.create(source=source)
        Content.objects.create(feed=feed, source=source, title='Title', url='www.content.tld')
        expected = {
            'id': feed.id,
            'source': OrderedDict([('id', source.id), ('name', 'Source'), ('slug', 'source'), ('source_type', 'security'), ('source_type_display', 'Security'), ('url', 'www.source.tld')]),
            'tags': [],
            'create_date': localtime(feed.create_date).isoformat().replace('+00:00', 'Z'),
            'write_date': localtime(feed.write_date).isoformat().replace('+00:00', 'Z'),
            'active': True,
            'tag_names': 'No Tags',
            'count': 1
        }
        serializer = FeedSerializer(feed)
        self.assertEquals(serializer.data, expected)


class ContentSerializerTestCase(TestCase):

    def test_content(self):
        source = Source.objects.create(name='Source', slug='source', source_type='security', url='www.source.tld')
        feed = Feed.objects.create(source=source)
        content = Content.objects.create(feed=feed, source=source, title='Title', url='www.content.tld')
        expected = {
            'id': content.id,
            'feed': OrderedDict([
                ('id', feed.id),
                ('source', OrderedDict([('id', source.id), ('name', 'Source'), ('slug', 'source'), ('source_type', 'security'), ('source_type_display', 'Security'), ('url', 'www.source.tld')])),
                ('tags', []),
                ('create_date', localtime(feed.create_date).isoformat().replace('+00:00', 'Z')),
                ('write_date', localtime(feed.write_date).isoformat().replace('+00:00', 'Z')),
                ('active', True),
                ('tag_names', 'No Tags'),
                ('count', 1)
            ]),
            'source': OrderedDict([
                ('id', source.id),
                ('name', 'Source'),
                ('slug', 'source'),
                ('source_type', 'security'),
                ('source_type_display', 'Security'),
                ('url', 'www.source.tld')
            ]),
            'tag': None,
            'title': 'Title',
            'url': 'www.content.tld',
            'viewed': False,
            'bookmarked': False,
            'create_date': localtime(content.create_date).isoformat().replace('+00:00', 'Z'),
        }
        serializer = ContentSerializer(content)
        self.assertEquals(serializer.data, expected)
