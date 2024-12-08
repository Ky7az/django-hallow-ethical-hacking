from django.test import TestCase

from HallowWriteup.models import Report, Tag, Website


class TagModelTestCase(TestCase):
    def setUp(self):
        Tag.objects.create(name='Tag', slug='tag')
        website = Website.objects.create(name='Website', slug='website')
        Report.objects.create(
            name='Report',
            slug='report',
            content='Content',
            website=website,
            task_type='ctf',
        )

    def test_count_property(self):
        tag = Tag.objects.get(slug='tag')
        report = Report.objects.get(slug='report')
        report.tags.add(tag)
        self.assertEqual(tag.count, report.tags.count())

    def test_string_method(self):
        tag = Tag.objects.get(slug='tag')
        self.assertEqual(str(tag), f'{tag.name}')


class WebsiteModelTestCase(TestCase):
    def setUp(self):
        Website.objects.create(
            name='Website', slug='website', url='https://www.website.tld'
        )

    def test_natural_key(self):
        website = Website.objects.get(slug='website')
        self.assertEqual(Website.objects.get_by_natural_key('website'), website)
        self.assertEqual(website.natural_key(), (website.slug,))

    def test_string_method(self):
        website = Website.objects.get(slug='website')
        self.assertEqual(str(website), f'{website.name}')


class ReportModelTestCase(TestCase):
    def setUp(self):
        website = Website.objects.create(name='Website', slug='website')
        Report.objects.create(
            name='Report',
            slug='report',
            website=website,
            task_type='ctf',
            content='Content',
        )

    def test_string_method(self):
        report = Report.objects.get(slug='report')
        self.assertEqual(str(report), f'{report.name}')
