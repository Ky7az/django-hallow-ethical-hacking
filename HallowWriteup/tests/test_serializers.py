from collections import OrderedDict

from django.test import TestCase
from django.utils.timezone import localtime

from HallowWriteup.models import Report, Tag, Website
from HallowWriteup.serializers import (
    ReportSerializer,
    TagSerializer,
    WebsiteSerializer
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
        self.assertEqual(serializer.data, expected)


class WebsiteSerializerTestCase(TestCase):

    def test_website(self):
        website = Website.objects.create(name='Website', slug='website', url='https://www.website.tld')
        expected = {
            'id': website.id,
            'name': 'Website',
            'slug': 'website',
            'url': 'https://www.website.tld'
        }
        serializer = WebsiteSerializer(website)
        self.assertEqual(serializer.data, expected)


class ReportSerializerTestCase(TestCase):

    def test_report(self):
        website = Website.objects.create(name='Website', slug='website', url='https://www.website.tld')
        report = Report.objects.create(
            name='Report',
            slug='report',
            website=website,
            task_type='ctf',
            task_platform='linux',
            task_url='https://www.task.tld',
            content='Content'
        )
        tag = Tag.objects.create(name='Tag', slug='tag')
        report.tags.add(tag)
        expected = {
            'id': report.id,
            'name': 'Report',
            'slug': 'report',
            'tags': [OrderedDict([('id', tag.id), ('name', 'Tag'), ('slug', 'tag'), ('count', 1)])],
            'website': OrderedDict([('id', website.id), ('name', 'Website'), ('slug', 'website'), ('url', 'https://www.website.tld')]),
            'task_type': 'ctf',
            'task_platform': 'linux',
            'task_type_display': 'Capture The Flag',
            'task_platform_display': 'Linux',
            'task_url': 'https://www.task.tld',
            'content': 'Content',
            'create_date': localtime(report.create_date).isoformat().replace('+00:00', 'Z'),
            'write_date': localtime(report.write_date).isoformat().replace('+00:00', 'Z'),
            'active': True
        }
        serializer = ReportSerializer(report)
        self.assertEqual(serializer.data, expected)
