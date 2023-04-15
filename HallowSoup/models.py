from django.db import models


## TAG ##

class Tag(models.Model):

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=64, unique=True)
    slug = models.SlugField(max_length=64, unique=True)

    @property
    def count(self):
        return self.articles.count

    def __str__(self):
        return f'{self.name}'

    class Meta:
        ordering = ['name']


## ARTICLE ##

class Article(models.Model):

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=128, unique=True)
    slug = models.SlugField(max_length=128, unique=True)
    content = models.TextField()
    tags = models.ManyToManyField('HallowSoup.Tag', related_name='articles')
    bookmarked = models.BooleanField(default=False)
    create_date = models.DateTimeField(auto_now_add=True)
    write_date = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        ordering = ['-write_date']
