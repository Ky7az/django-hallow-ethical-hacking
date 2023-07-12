from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from rest_framework.test import APITestCase

from HallowWriteup.models import Report, Tag, Website


class TagAPITestCase(APITestCase):

    def setUp(self):
        for x in range(1, 3):
            Tag.objects.create(name=f'Tag {x}', slug=f'tag-{x}')

    def authenticate_user(self):
        user = User.objects.create_user('user', 'user@user.tld', 'password')
        self.client.force_authenticate(user=user)

    def test_list_tags(self):
        # Unauthorized
        response = self.client.get('/api/writeup/tags/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # Authorized
        self.authenticate_user()
        response = self.client.get('/api/writeup/tags/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_create_tag(self):
        data = {
            'name': 'Tag',
            'slug': 'tag'
        }
        # Unauthorized
        response = self.client.post('/api/writeup/tags/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # Authorized
        self.authenticate_user()
        response = self.client.post('/api/writeup/tags/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Tag.objects.count(), 3)
        self.assertEqual(Tag.objects.get(slug='tag').name, 'Tag')

    def test_update_tag(self):
        tag_1 = Tag.objects.get(slug='tag-1')
        data = {
            'name': 'Tag X',
            'slug': 'tag-x'
        }
        # Unauthorized
        response = self.client.patch(f'/api/writeup/tags/{tag_1.slug}/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # Authorized
        self.authenticate_user()
        response = self.client.patch(f'/api/writeup/tags/{tag_1.slug}/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        tag_1.refresh_from_db()
        self.assertEqual(tag_1.name, data['name'])
        self.assertEqual(tag_1.slug, data['slug'])

    def test_delete_tag(self):
        tag_1 = Tag.objects.get(slug='tag-1')
        # Unauthorized
        response = self.client.delete(f'/api/writeup/tags/{tag_1.slug}/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # Authorized
        self.authenticate_user()
        response = self.client.delete(f'/api/writeup/tags/{tag_1.slug}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Tag.objects.count(), 1)
        with self.assertRaises(ObjectDoesNotExist):
            Tag.objects.get(slug='tag-1')


class WebsiteAPITestCase(APITestCase):

    def setUp(self):
        for x in range(1, 3):
            Website.objects.create(
                name=f'Website {x}',
                slug=f'website-{x}',
                url=f'https://www.website-{x}.tld'
            )

    def authenticate_user(self):
        user = User.objects.create_user('user', 'user@user.tld', 'password')
        self.client.force_authenticate(user=user)

    def test_list_websites(self):
        # Unauthorized
        response = self.client.get('/api/writeup/websites/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # Authorized
        self.authenticate_user()
        response = self.client.get('/api/writeup/websites/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_create_website(self):
        data = {
            'name': 'Website',
            'slug': 'website'
        }
        # Unauthorized
        response = self.client.post('/api/writeup/websites/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # Authorized
        self.authenticate_user()
        response = self.client.post('/api/writeup/websites/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Website.objects.count(), 3)
        self.assertEqual(Website.objects.get(slug='website').name, 'Website')

    def test_update_website(self):
        website_1 = Website.objects.get(slug='website-1')
        data = {
            'name': 'Website X',
            'slug': 'website-x'
        }
        # Unauthorized
        response = self.client.patch(f'/api/writeup/websites/{website_1.slug}/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # Authorized
        self.authenticate_user()
        response = self.client.patch(f'/api/writeup/websites/{website_1.slug}/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        website_1.refresh_from_db()
        self.assertEqual(website_1.name, data['name'])
        self.assertEqual(website_1.slug, data['slug'])

    def test_delete_website(self):
        website_1 = Website.objects.get(slug='website-1')
        # Unauthorized
        response = self.client.delete(f'/api/writeup/websites/{website_1.slug}/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # Authorized
        self.authenticate_user()
        response = self.client.delete(f'/api/writeup/websites/{website_1.slug}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Website.objects.count(), 1)
        with self.assertRaises(ObjectDoesNotExist):
            Website.objects.get(slug='website-1')


class ReportAPITestCase(APITestCase):

    def setUp(self):
        tag = Tag.objects.create(name='Tag', slug='tag')
        website = Website.objects.create(name='Website', slug='website')
        for x in range(1, 3):
            report = Report.objects.create(
                name=f'Report {x}',
                slug=f'report-{x}',
                website=website,
                task_type='ctf',
                task_platform='linux'
            )
            report.tags.add(tag)

    def authenticate_user(self):
        user = User.objects.create_user('user', 'user@user.tld', 'password')
        self.client.force_authenticate(user=user)

    def test_list_reports(self):
        # Unauthorized
        response = self.client.get('/api/writeup/reports/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # Authorized
        self.authenticate_user()
        response = self.client.get('/api/writeup/reports/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 2)
        self.assertEqual(len(response.data['results']), 2)

    def test_list_reports_with_filters(self):
        # Authorized
        self.authenticate_user()

        # name_or_content
        response = self.client.get('/api/writeup/reports/?name_or_content=x')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 0)
        self.assertEqual(len(response.data['results']), 0)

        response = self.client.get('/api/writeup/reports/?name_or_content=1')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(len(response.data['results']), 1)

        # tags
        response = self.client.get('/api/writeup/reports/?tags=x')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['tags'][0].code, 'invalid_choice')

        response = self.client.get('/api/writeup/reports/?tags=tag')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 2)
        self.assertEqual(len(response.data['results']), 2)

        # website
        response = self.client.get('/api/writeup/reports/?website=x')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['website'][0].code, 'invalid_choice')

        response = self.client.get('/api/writeup/reports/?website=website')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 2)
        self.assertEqual(len(response.data['results']), 2)

        # task_type
        response = self.client.get('/api/writeup/reports/?task_type=x')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['task_type'][0].code, 'invalid_choice')

        response = self.client.get('/api/writeup/reports/?task_type=ctf')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 2)
        self.assertEqual(len(response.data['results']), 2)

        # task_platform
        response = self.client.get('/api/writeup/reports/?task_platform=x')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['task_platform'][0].code, 'invalid_choice')

        response = self.client.get('/api/writeup/reports/?task_platform=linux')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 2)
        self.assertEqual(len(response.data['results']), 2)

    def test_create_report(self):
        website = Website.objects.get(slug='website')
        data = {
            'name': 'Report',
            'slug': 'report',
            'website_id': website.id,
            'task_type': 'ctf',
            'task_platform': 'linux',
            'content': 'Content',
            'tags': [
                {
                    'name': 'Tag 1',
                    'slug': 'tag-1'
                },
                {
                    'name': 'Tag 2',
                    'slug': 'tag-2'
                }
            ]
        }
        # Unauthorized
        response = self.client.post('/api/writeup/reports/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # Authorized
        self.authenticate_user()
        response = self.client.post('/api/writeup/reports/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Report.objects.count(), 3)
        report = Report.objects.get(slug='report')
        self.assertEqual(report.name, 'Report')
        self.assertEqual(report.tags.count(), 2)
        self.assertEqual([x.name for x in report.tags.all()], ['Tag 1', 'Tag 2'])

    def test_update_report(self):
        report_1 = Report.objects.get(slug='report-1')
        self.assertEqual(report_1.tags.count(), 1)
        data = {
            'content': 'Content X',
            'tags': [
                {
                    'name': 'Tag 1',
                    'slug': 'tag-1'
                },
                {
                    'name': 'Tag 2',
                    'slug': 'tag-2'
                }
            ]
        }
        # Unauthorized
        response = self.client.patch(f'/api/writeup/reports/{report_1.slug}/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # Authorized
        self.authenticate_user()
        response = self.client.patch(f'/api/writeup/reports/{report_1.slug}/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        report_1.refresh_from_db()
        self.assertEqual(report_1.content, data['content'])
        self.assertEqual(report_1.tags.count(), 2)
        self.assertEqual([x.name for x in report_1.tags.all()], ['Tag 1', 'Tag 2'])

    def test_delete_report(self):
        report_1 = Report.objects.get(slug='report-1')
        # Unauthorized
        response = self.client.delete(f'/api/writeup/reports/{report_1.slug}/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # Authorized
        self.authenticate_user()
        response = self.client.delete(f'/api/writeup/reports/{report_1.slug}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Report.objects.count(), 1)
        with self.assertRaises(ObjectDoesNotExist):
            Report.objects.get(slug='report-1')
