import datetime
import re
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup
from django.db import models


# TAG

class Tag(models.Model):

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=64, unique=True)
    slug = models.SlugField(max_length=64, unique=True)

    @property
    def count(self):
        return Content.objects.filter(tag=self).count()

    def __str__(self):
        return f'{self.name}'

    class Meta:
        ordering = ['name']


# SOURCE

class SourceManager(models.Manager):

    def get_by_natural_key(self, slug):
        return self.get(slug=slug)


class Source(models.Model):

    SOURCE_TYPES = [
        ('', ''),
        ('exploit', 'Exploit'),
        ('security', 'Security'),
        ('technology', 'Technology'),
        ('vulnerability', 'Vulnerability')
    ]

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=64, unique=True)
    slug = models.SlugField(max_length=64, unique=True)
    source_type = models.CharField(max_length=13, choices=SOURCE_TYPES)
    url = models.CharField(max_length=256)

    objects = SourceManager()

    def natural_key(self):
        return (self.slug,)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        ordering = ['name']

    def get_base_url(self, url):
        parsed = urlparse(url)
        return f'{parsed.scheme}://{parsed.netloc}'

    def scrap_source(self, tags):
        slug = self.slug.replace('-', '_')
        if scrap_fnct := getattr(self, f'scrap_source_{slug}', False):
            return scrap_fnct(self.url, tags)
        else:
            return []

    def scrap_source_cert_fr(self, url, tags):
        base_url = self.get_base_url(url)

        for path in ['alerte', 'avis', 'actualite']:
            url_path = f'{url}/{path}/'

            r = requests.get(url_path)
            r.encoding = 'utf-8'
            soup = BeautifulSoup(r.text, 'html.parser')

            for div in soup.find_all('div', class_='item-title'):
                a = div.h3.a
                href = a['href']
                curl = f'{base_url}{href}'

                yield {
                    'source': self,
                    'title': a.string,
                    'url': curl
                }

    def scrap_source_cve_details(self, url, tags):
        base_url = self.get_base_url(url)

        for tag in tags.all():
            r = requests.get(f'{url}vulnerability-search.php?f=1&vendor=&product={tag.name}&cveid=&msid=&bidno=&cweid=&cvssscoremin=&cvssscoremax=&psy=&psm=&pey=&pem=&usy=&usm=&uey=&uem=')
            soup = BeautifulSoup(r.text, 'html.parser')

            for tr in soup.find_all('tr', class_='srrowns')[:10]:
                td = tr.find_all('td')[3]
                href = td.a['href']
                curl = f'{base_url}{href}'

                yield {
                    'source': self,
                    'tag': tag,
                    'title': td.string,
                    'url': curl
                }

    def scrap_source_debian(self, url, tags):
        today_year = str(datetime.date.today().year)
        r = requests.get(url + today_year)
        soup = BeautifulSoup(r.text, 'html.parser')

        for strong in soup.find_all('strong')[:10]:
            if strong.a and strong.a.string.startswith('DSA'):
                a = strong.a
                href = a['href']
                curl = f'{url}{today_year}/{href}'

                yield {
                    'source': self,
                    'title': a.string,
                    'url': curl
                }

    def scrap_source_drupal(self, url, tags):
        base_url = self.get_base_url(url)
        r = requests.get(url)
        soup = BeautifulSoup(r.text, 'html.parser')

        for div in soup.find_all('div', class_=re.compile('^views-row')):
            h2 = div.div.h2
            href = h2.a['href']
            curl = f'{base_url}{href}'

            yield {
                'source': self,
                'title': h2.string,
                'url': curl
            }

    def scrap_source_exploit_db(self, url, tags):
        base_url = self.get_base_url(url)
        r = requests.get('https://gitlab.com/exploit-database/exploitdb/-/raw/main/files_exploits.csv')
        csv_rows = r.text.split('\n')

        for tag in tags.all():
            rows = []
            for r in csv_rows[1:]:
                csv_cols = r.split(',')
                if len(csv_cols) == 17 and tag.name.lower() in csv_cols[2].lower():
                    csv_cols[0] = int(csv_cols[0])
                    rows.append(csv_cols)

            rows.sort(key=lambda c: c[0])
            for row in rows[-10:]:
                yield {
                    'source': self,
                    'tag': tag,
                    'title': row[2],
                    'url': f'{base_url}/exploits/{row[0]}'
                }

    def scrap_source_hackernews(self, url, tags):
        base_url = self.get_base_url(url)
        r = requests.get(url)
        soup = BeautifulSoup(r.text, 'html.parser')

        for span in soup.find_all('span', class_='titleline'):
            a = span.a
            href = a['href']
            curl = href if href.startswith('http') else f'{base_url}/{href}'
            yield {
                'source': self,
                'title': a.string,
                'url': curl
            }

    def scrap_source_nist_nvd(self, url, tags):
        api_url = 'https://services.nvd.nist.gov/rest/json/cves/2.0'

        for tag in tags.all():
            r = requests.get(f'{api_url}?keywordSearch={tag.name}&resultsPerPage=0')
            if total := int(r.json()['totalResults']):
                start_index = total - 10 if total > 10 else 0
                r = requests.get(f'{api_url}?keywordSearch={tag.name}&resultsPerPage=10&startIndex={start_index}')
                data = r.json()

                for vuln in data['vulnerabilities']:
                    cve_id = vuln['cve']['id']
                    curl = f'{url}vuln/detail/{cve_id}'
                    yield {
                        'source': self,
                        'tag': tag,
                        'title': cve_id,
                        'url': curl
                    }

    def scrap_source_packetstorm(self, url, tags):
        base_url = self.get_base_url(url)

        for tag in tags.all():
            r = requests.get(f'{url}search/?q={tag.name}&s=files')
            soup = BeautifulSoup(r.text, 'html.parser')

            for dl in soup.find_all('dl'):
                if a := dl.dt.a:
                    href = a['href']
                    curl = f'{base_url}{href}'

                    yield {
                        'source': self,
                        'tag': tag,
                        'title': a.string,
                        'url': curl
                    }

    def scrap_source_thehackernews(self, url, tags):
        r = requests.get(url)
        soup = BeautifulSoup(r.text, 'html.parser')

        for post in soup.find_all('div', class_='body-post'):
            h2 = post.find('h2')
            link = post.find('a', class_='story-link')

            if h2.string:
                yield {
                    'source': self,
                    'title': h2.string,
                    'url': link['href']
                }

    def scrap_source_ubuntu(self, url, tags):
        base_url = self.get_base_url(url)
        r = requests.get(url)
        soup = BeautifulSoup(r.text, 'html.parser')

        for art in soup.find_all('article'):
            h3 = art.h3
            href = h3.a['href']
            curl = f'{base_url}{href}'

            yield {
                'source': self,
                'title': h3.a.string,
                'url': curl
            }


# FEED

class Feed(models.Model):

    id = models.AutoField(primary_key=True)
    source = models.OneToOneField('HallowWatch.Source', on_delete=models.CASCADE, null=True, unique=True)
    tags = models.ManyToManyField('HallowWatch.Tag', related_name='feeds')
    create_date = models.DateTimeField(auto_now_add=True)
    write_date = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)
    celery_task_id = models.CharField(max_length=64, blank=True)

    @property
    def tag_names(self):
        return ', '.join(self.tags.values_list('name', flat=True)) or 'No Tags'

    @property
    def count(self):
        return Content.objects.filter(feed=self).count()

    def __str__(self):
        return f'{self.source.name} ({self.tag_names})'

    class Meta:
        ordering = ['-write_date']

    def scrap_feed(self):
        for content_data in self.source.scrap_source(self.tags) or []:
            content_data.update(feed=self)
            yield content_data


# CONTENT

class Content(models.Model):

    id = models.AutoField(primary_key=True)
    feed = models.ForeignKey(Feed, on_delete=models.CASCADE)
    source = models.ForeignKey(Source, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE, blank=True, null=True)
    title = models.CharField(max_length=256)
    url = models.CharField(max_length=256, unique=True)
    viewed = models.BooleanField(default=False)
    bookmarked = models.BooleanField(default=False)
    create_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.url}'

    class Meta:
        ordering = ['-create_date']
