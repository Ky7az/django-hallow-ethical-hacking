from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from rest_framework.test import APITestCase

from HallowWatch.models import Content, Feed, Source, Tag


class TagAPITestCase(APITestCase):
    def setUp(self):
        for x in range(1, 3):
            Tag.objects.create(name=f'Tag {x}', slug=f'tag-{x}')

    def authenticate_user(self):
        user = User.objects.create_user('user', 'user@user.tld', 'password')
        self.client.force_authenticate(user=user)

    def test_list_tags(self):
        # Unauthorized
        response = self.client.get('/api/watch/tags/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # Authorized
        self.authenticate_user()
        response = self.client.get('/api/watch/tags/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_create_tag(self):
        data = {'name': 'Tag', 'slug': 'tag'}
        # Unauthorized
        response = self.client.post('/api/watch/tags/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # Authorized
        self.authenticate_user()
        response = self.client.post('/api/watch/tags/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Tag.objects.count(), 3)
        self.assertEqual(Tag.objects.get(slug='tag').name, 'Tag')

    def test_update_tag(self):
        tag_1 = Tag.objects.get(slug='tag-1')
        data = {'name': 'Tag X', 'slug': 'tag-x'}
        # Unauthorized
        response = self.client.patch(
            f'/api/watch/tags/{tag_1.slug}/', data, format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # Authorized
        self.authenticate_user()
        response = self.client.patch(
            f'/api/watch/tags/{tag_1.slug}/', data, format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        tag_1.refresh_from_db()
        self.assertEqual(tag_1.name, data['name'])
        self.assertEqual(tag_1.slug, data['slug'])

    def test_delete_tag(self):
        tag_1 = Tag.objects.get(slug='tag-1')
        # Unauthorized
        response = self.client.delete(f'/api/watch/tags/{tag_1.slug}/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # Authorized
        self.authenticate_user()
        response = self.client.delete(f'/api/watch/tags/{tag_1.slug}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Tag.objects.count(), 1)
        with self.assertRaises(ObjectDoesNotExist):
            Tag.objects.get(slug='tag-1')


class SourceAPITestCase(APITestCase):
    def setUp(self):
        for x in range(1, 3):
            Source.objects.create(
                name=f'Source {x}',
                slug=f'source-{x}',
                source_type='security',
                url=f'www.source-{x}.tld',
            )

    def authenticate_user(self):
        user = User.objects.create_user('user', 'user@user.tld', 'password')
        self.client.force_authenticate(user=user)

    def test_list_sources(self):
        # Unauthorized
        response = self.client.get('/api/watch/sources/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # Authorized
        self.authenticate_user()
        response = self.client.get('/api/watch/sources/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_create_source(self):
        data = {
            'name': 'Source',
            'slug': 'source',
            'source_type': 'security',
            'source_type_display': 'Security',
            'url': 'www.source.tld',
        }
        # Unauthorized
        response = self.client.post('/api/watch/sources/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # Authorized
        self.authenticate_user()
        response = self.client.post('/api/watch/sources/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Source.objects.count(), 3)
        self.assertEqual(Source.objects.get(slug='source').name, data['name'])

    def test_update_source(self):
        source_1 = Source.objects.get(slug='source-1')
        data = {
            'name': 'Source X',
            'slug': 'source-x',
            'source_type': 'security',
            'source_type_display': 'Security',
            'url': 'www.source-x.tld',
        }
        # Unauthorized
        response = self.client.patch(
            f'/api/watch/sources/{source_1.slug}/', data, format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # Authorized
        self.authenticate_user()
        response = self.client.patch(
            f'/api/watch/sources/{source_1.slug}/', data, format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        source_1.refresh_from_db()
        self.assertEqual(source_1.name, data['name'])
        self.assertEqual(source_1.slug, data['slug'])
        self.assertEqual(source_1.url, data['url'])

    def test_delete_source(self):
        source_1 = Source.objects.get(slug='source-1')
        # Unauthorized
        response = self.client.delete(f'/api/watch/sources/{source_1.slug}/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # Authorized
        self.authenticate_user()
        response = self.client.delete(f'/api/watch/sources/{source_1.slug}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Source.objects.count(), 1)
        with self.assertRaises(ObjectDoesNotExist):
            Source.objects.get(slug='source-1')


class FeedAPITestCase(APITestCase):
    def setUp(self):
        for x in range(1, 3):
            source = Source.objects.create(
                name=f'Source {x}',
                slug=f'source-{x}',
                source_type='security',
                url=f'www.source-{x}.tld',
            )
            Feed.objects.create(source=source)

    def authenticate_user(self):
        user = User.objects.create_user('user', 'user@user.tld', 'password')
        self.client.force_authenticate(user=user)

    def test_list_feeds(self):
        # Unauthorized
        response = self.client.get('/api/watch/feeds/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # Authorized
        self.authenticate_user()
        response = self.client.get('/api/watch/feeds/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_create_feed(self):
        source = Source.objects.create(
            name='Source', slug='source', source_type='security', url='www.source.tld'
        )
        data = {
            'source_id': source.id,
            'tags': [
                {'name': 'Tag 1', 'slug': 'tag-1'},
                {'name': 'Tag 2', 'slug': 'tag-2'},
            ],
        }
        # Unauthorized
        response = self.client.post('/api/watch/feeds/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # Authorized
        self.authenticate_user()
        response = self.client.post('/api/watch/feeds/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Feed.objects.count(), 3)
        self.assertEqual(Feed.objects.get(source=source).id, response.data['id'])

    def test_update_feed(self):
        source_1 = Source.objects.get(slug='source-1')
        feed_1 = Feed.objects.get(source=source_1)
        source = Source.objects.create(
            name='Source x',
            slug='source-x',
            source_type='security',
            url='www.source-x.tld',
        )
        data = {'source_id': source.id}
        # Unauthorized
        response = self.client.patch(
            f'/api/watch/feeds/{feed_1.id}/', data, format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # Authorized
        self.authenticate_user()
        response = self.client.patch(
            f'/api/watch/feeds/{feed_1.id}/', data, format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        feed_1.refresh_from_db()
        self.assertEqual(feed_1.source.id, data['source_id'])

    def test_delete_feed(self):
        source_1 = Source.objects.get(slug='source-1')
        feed_1 = Feed.objects.get(source=source_1)
        # Unauthorized
        response = self.client.delete(f'/api/watch/feeds/{feed_1.id}/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # Authorized
        self.authenticate_user()
        response = self.client.delete(f'/api/watch/feeds/{feed_1.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Feed.objects.count(), 1)
        with self.assertRaises(ObjectDoesNotExist):
            Feed.objects.get(source=source_1)


class ContentAPITestCase(APITestCase):
    def setUp(self):
        tag = Tag.objects.create(name='Tag', slug='tag')
        for x in range(1, 3):
            source = Source.objects.create(
                name=f'Source {x}',
                slug=f'source-{x}',
                source_type='security',
                url=f'www.source-{x}.tld',
            )
            feed = Feed.objects.create(source=source)
            Content.objects.create(
                feed=feed,
                source=source,
                tag=tag,
                title=f'Title-{x}',
                url=f'www.content-{x}.tld',
            )

    def authenticate_user(self):
        user = User.objects.create_user('user', 'user@user.tld', 'password')
        self.client.force_authenticate(user=user)

    def test_list_contents(self):
        # Unauthorized
        response = self.client.get('/api/watch/contents/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # Authorized
        self.authenticate_user()
        response = self.client.get('/api/watch/contents/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)

    def test_list_contents_with_filters(self):
        # Authorized
        self.authenticate_user()

        # title
        response = self.client.get('/api/watch/contents/?title=x')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 0)
        self.assertEqual(len(response.data['results']), 0)

        response = self.client.get('/api/watch/contents/?title=1')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(len(response.data['results']), 1)

        # tags
        response = self.client.get('/api/watch/contents/?tag=x')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['tag'][0].code, 'invalid_choice')

        response = self.client.get('/api/watch/contents/?tag=tag')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 2)
        self.assertEqual(len(response.data['results']), 2)

        # source_type
        response = self.client.get('/api/watch/contents/?source_type=x')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['source_type'][0].code, 'invalid_choice')

        response = self.client.get('/api/watch/contents/?source_type=security')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 2)
        self.assertEqual(len(response.data['results']), 2)

        # viewed
        response = self.client.get('/api/watch/contents/?viewed=true')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 0)
        self.assertEqual(len(response.data['results']), 0)

        response = self.client.get('/api/watch/contents/?viewed=false')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 2)
        self.assertEqual(len(response.data['results']), 2)

        # bookmarked
        response = self.client.get('/api/watch/contents/?bookmarked=true')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 0)
        self.assertEqual(len(response.data['results']), 0)

        response = self.client.get('/api/watch/contents/?bookmarked=false')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 2)
        self.assertEqual(len(response.data['results']), 2)

    def test_create_content(self):
        source = Source.objects.create(
            name='Source', slug='source', source_type='security', url='www.source.tld'
        )
        feed = Feed.objects.create(source=source)
        data = {
            'feed_id': feed.id,
            'source_id': source.id,
            'title': 'Title',
            'url': 'www.source.tld',
        }
        # Unauthorized
        response = self.client.post('/api/watch/contents/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # Authorized
        self.authenticate_user()
        response = self.client.post('/api/watch/contents/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Content.objects.count(), 3)
        self.assertEqual(
            Content.objects.get(feed=feed, source=source).id, response.data['id']
        )

    def test_update_content(self):
        source_1 = Source.objects.get(slug='source-1')
        feed_1 = Feed.objects.get(source=source_1)
        content_1 = Content.objects.get(feed=feed_1, source=source_1)
        source = Source.objects.create(
            name='Source x',
            slug='source-x',
            source_type='security',
            url='www.source-x.tld',
        )
        feed = Feed.objects.create(source=source)
        data = {
            'feed_id': feed.id,
            'source_id': source.id,
            'title': 'Title X',
            'url': 'www.content-x.tld',
        }
        # Unauthorized
        response = self.client.patch(
            f'/api/watch/contents/{content_1.id}/', data, format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # Authorized
        self.authenticate_user()
        response = self.client.patch(
            f'/api/watch/contents/{content_1.id}/', data, format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        content_1.refresh_from_db()
        self.assertEqual(content_1.feed.id, data['feed_id'])
        self.assertEqual(content_1.source.id, data['source_id'])
        self.assertEqual(content_1.title, data['title'])
        self.assertEqual(content_1.url, data['url'])

    def test_delete_content(self):
        source_1 = Source.objects.get(slug='source-1')
        feed_1 = Feed.objects.get(source=source_1)
        content_1 = Content.objects.get(feed=feed_1, source=source_1)
        # Unauthorized
        response = self.client.delete(f'/api/watch/contents/{content_1.id}/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # Authorized
        self.authenticate_user()
        response = self.client.delete(f'/api/watch/contents/{content_1.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Content.objects.count(), 1)
        with self.assertRaises(ObjectDoesNotExist):
            Content.objects.get(feed=feed_1, source=source_1)
