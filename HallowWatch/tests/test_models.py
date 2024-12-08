from django.test import TestCase

from HallowWatch.models import Content, Feed, Source, Tag


class TagModelTestCase(TestCase):
    def setUp(self):
        tag = Tag.objects.create(name='Tag', slug='tag')
        source = Source.objects.create(
            name='Source', slug='source', source_type='security', url='www.source.tld'
        )
        feed = Feed.objects.create(source=source)
        Content.objects.create(
            feed=feed, source=source, tag=tag, title='Title', url='www.content.tld'
        )

    def test_count_property(self):
        tag = Tag.objects.get(slug='tag')
        content = Content.objects.filter(tag=tag)
        self.assertEqual(tag.count, content.count())

    def test_string_method(self):
        tag = Tag.objects.get(slug='tag')
        self.assertEqual(str(tag), f'{tag.name}')


class SourceModelTestCase(TestCase):
    def setUp(self):
        Source.objects.create(
            name='Source', slug='source', source_type='security', url='www.source.tld'
        )

    def test_natural_key(self):
        source = Source.objects.get(slug='source')
        self.assertEqual(Source.objects.get_by_natural_key('source'), source)
        self.assertEqual(source.natural_key(), (source.slug,))

    def test_string_method(self):
        source = Source.objects.get(slug='source')
        self.assertEqual(str(source), f'{source.name}')


class FeedModelTestCase(TestCase):
    def setUp(self):
        source = Source.objects.create(
            name='Source', slug='source', source_type='security', url='www.source.tld'
        )
        feed = Feed.objects.create(source=source)
        Content.objects.create(
            feed=feed, source=source, title='Title', url='www.content.tld'
        )

    def test_tag_names_property(self):
        feed = Feed.objects.get()
        self.assertEqual(feed.tag_names, 'No Tags')
        tag_1 = Tag.objects.create(name='Tag 1', slug='tag_1')
        feed.tags.add(tag_1)
        self.assertEqual(feed.tag_names, 'Tag 1')
        tag_2 = Tag.objects.create(name='Tag 2', slug='tag_2')
        feed.tags.add(tag_2)
        self.assertEqual(feed.tag_names, 'Tag 1, Tag 2')

    def test_count_property(self):
        feed = Feed.objects.get()
        content = Content.objects.filter(feed=feed)
        self.assertEqual(feed.count, content.count())

    def test_string_method(self):
        feed = Feed.objects.get()
        self.assertEqual(str(feed), f'{feed.source.name} ({feed.tag_names})')


class ContentModelTestCase(TestCase):
    def setUp(self):
        source = Source.objects.create(
            name='Source', slug='source', source_type='security', url='www.source.tld'
        )
        feed = Feed.objects.create(source=source)
        Content.objects.create(
            feed=feed, source=source, title='Title', url='www.content.tld'
        )

    def test_string_method(self):
        content = Content.objects.get()
        self.assertEqual(str(content), f'{content.url}')
