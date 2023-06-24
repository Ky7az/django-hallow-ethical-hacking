from django.db import models


# TAG

class Tag(models.Model):

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=64, unique=True)
    slug = models.SlugField(max_length=64, unique=True)

    @property
    def count(self):
        return self.reports.count

    def __str__(self):
        return f'{self.name}'

    class Meta:
        ordering = ['name']


# WEBSITE

class WebsiteManager(models.Manager):

    def get_by_natural_key(self, slug):
        return self.get(slug=slug)


class Website(models.Model):

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=64, unique=True)
    slug = models.SlugField(max_length=64, unique=True)
    url = models.CharField(max_length=256, blank=True)

    objects = WebsiteManager()

    def natural_key(self):
        return (self.slug,)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        ordering = ['name']


# REPORT

class Report(models.Model):

    TASK_TYPES = [
        ('', ''),
        ('bugbounty', 'Bug Bounty'),
        ('ctf', 'Capture The Flag')
    ]
    TASK_PLATFORMS = [
        ('', ''),
        ('linux', 'Linux'),
        ('windows', 'Windows')
    ]

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=64, unique=True)
    slug = models.SlugField(max_length=64, unique=True)
    tags = models.ManyToManyField('HallowWriteup.Tag', related_name='reports')
    website = models.ForeignKey(Website, on_delete=models.CASCADE)
    task_type = models.CharField(max_length=9, choices=TASK_TYPES)
    task_platform = models.CharField(max_length=7, choices=TASK_PLATFORMS, blank=True)
    task_url = models.CharField(max_length=256, blank=True)
    content = models.TextField()
    create_date = models.DateTimeField(auto_now_add=True)
    write_date = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        ordering = ['-write_date']
