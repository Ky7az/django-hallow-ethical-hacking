from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from rest_framework.test import APITestCase

from HallowSoup.models import Article, Tag


class TagAPITestCase(APITestCase):

    def setUp(self):
        for x in range(1, 3):
            Tag.objects.create(name=f'Tag {x}', slug=f'tag-{x}')

    def authenticate_user(self):
        user = User.objects.create_user('user', 'user@user.tld', 'password')
        self.client.force_authenticate(user=user)

    def test_list_tags(self):
        # Unauthorized
        response = self.client.get('/api/soup/tags/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # Authorized
        self.authenticate_user()
        response = self.client.get('/api/soup/tags/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_create_tag(self):
        data = {
            'name': 'Tag',
            'slug': 'tag'
        }
        # Unauthorized
        response = self.client.post('/api/soup/tags/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # Authorized
        self.authenticate_user()
        response = self.client.post('/api/soup/tags/', data, format='json')
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
        response = self.client.patch(f'/api/soup/tags/{tag_1.slug}/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # Authorized
        self.authenticate_user()
        response = self.client.patch(f'/api/soup/tags/{tag_1.slug}/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        tag_1.refresh_from_db()
        self.assertEqual(tag_1.name, data['name'])
        self.assertEqual(tag_1.slug, data['slug'])

    def test_delete_tag(self):
        tag_1 = Tag.objects.get(slug='tag-1')
        # Unauthorized
        response = self.client.delete(f'/api/soup/tags/{tag_1.slug}/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # Authorized
        self.authenticate_user()
        response = self.client.delete(f'/api/soup/tags/{tag_1.slug}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Tag.objects.count(), 1)
        with self.assertRaises(ObjectDoesNotExist):
            Tag.objects.get(slug='tag-1')


class ArticleAPITestCase(APITestCase):

    def setUp(self):
        tag = Tag.objects.create(name='Tag', slug='tag')
        for x in range(1, 3):
            article = Article.objects.create(name=f'Article {x}', slug=f'article-{x}', content=f'Content {x}')
            article.tags.add(tag)

    def authenticate_user(self):
        user = User.objects.create_user('user', 'user@user.tld', 'password')
        self.client.force_authenticate(user=user)

    def test_list_articles(self):
        # Unauthorized
        response = self.client.get('/api/soup/articles/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # Authorized
        self.authenticate_user()
        response = self.client.get('/api/soup/articles/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 2)
        self.assertEqual(len(response.data['results']), 2)

    def test_list_articles_with_filters(self):
        # Authorized
        self.authenticate_user()

        # name_or_content
        response = self.client.get('/api/soup/articles/?name_or_content=x')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 0)
        self.assertEqual(len(response.data['results']), 0)

        response = self.client.get('/api/soup/articles/?name_or_content=1')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(len(response.data['results']), 1)

        # tags
        response = self.client.get('/api/soup/articles/?tags=x')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['tags'][0].code, 'invalid_choice')

        response = self.client.get('/api/soup/articles/?tags=tag')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 2)
        self.assertEqual(len(response.data['results']), 2)

        # bookmarked
        response = self.client.get('/api/soup/articles/?bookmarked=true')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 0)
        self.assertEqual(len(response.data['results']), 0)

        response = self.client.get('/api/soup/articles/?bookmarked=false')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 2)
        self.assertEqual(len(response.data['results']), 2)

    def test_create_article(self):
        data = {
            'name': 'Article',
            'slug': 'article',
            'content': 'Content',
            'tags': [{
                'name': 'Tag 1',
                'slug': 'tag-1'
            }, {
                'name': 'Tag 2',
                'slug': 'tag-2'
            }]
        }
        # Unauthorized
        response = self.client.post('/api/soup/articles/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # Authorized
        self.authenticate_user()
        response = self.client.post('/api/soup/articles/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Article.objects.count(), 3)
        article = Article.objects.get(slug='article')
        self.assertEqual(article.name, 'Article')
        self.assertEqual(article.tags.count(), 2)
        self.assertEqual([x.name for x in article.tags.all()], ['Tag 1', 'Tag 2'])

    def test_update_article(self):
        article_1 = Article.objects.get(slug='article-1')
        self.assertEqual(article_1.tags.count(), 1)
        data = {
            'content': 'Content X',
            'bookmarked': True,
            'tags': [{
                'name': 'Tag 1',
                'slug': 'tag-1'
            }, {
                'name': 'Tag 2',
                'slug': 'tag-2'
            }]
        }
        # Unauthorized
        response = self.client.patch(f'/api/soup/articles/{article_1.slug}/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # Authorized
        self.authenticate_user()
        response = self.client.patch(f'/api/soup/articles/{article_1.slug}/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        article_1.refresh_from_db()
        self.assertEqual(article_1.content, data['content'])
        self.assertEqual(article_1.bookmarked, data['bookmarked'])
        self.assertEqual(article_1.tags.count(), 2)
        self.assertEqual([x.name for x in article_1.tags.all()], ['Tag 1', 'Tag 2'])

    def test_delete_article(self):
        article_1 = Article.objects.get(slug='article-1')
        # Unauthorized
        response = self.client.delete(f'/api/soup/articles/{article_1.slug}/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # Authorized
        self.authenticate_user()
        response = self.client.delete(f'/api/soup/articles/{article_1.slug}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Article.objects.count(), 1)
        with self.assertRaises(ObjectDoesNotExist):
            Article.objects.get(slug='article-1')
