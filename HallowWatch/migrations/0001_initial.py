# Generated by Django 3.2.16 on 2023-04-02 20:36

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='Source',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=64, unique=True)),
                ('slug', models.SlugField(max_length=64, unique=True)),
                (
                    'source_type',
                    models.CharField(
                        choices=[
                            ('', ''),
                            ('exploit', 'Exploit'),
                            ('security', 'Security'),
                            ('technology', 'Technology'),
                            ('vulnerability', 'Vulnerability'),
                        ],
                        max_length=13,
                    ),
                ),
                ('url', models.CharField(max_length=256)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=64, unique=True)),
                ('slug', models.SlugField(max_length=64, unique=True)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Feed',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('write_date', models.DateTimeField(auto_now=True)),
                ('active', models.BooleanField(default=True)),
                ('celery_task_id', models.CharField(blank=True, max_length=64)),
                (
                    'source',
                    models.OneToOneField(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to='HallowWatch.source',
                    ),
                ),
                (
                    'tags',
                    models.ManyToManyField(related_name='feeds', to='HallowWatch.Tag'),
                ),
            ],
            options={
                'ordering': ['-write_date'],
            },
        ),
        migrations.CreateModel(
            name='Content',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=256)),
                ('url', models.CharField(max_length=256, unique=True)),
                ('viewed', models.BooleanField(default=False)),
                ('bookmarked', models.BooleanField(default=False)),
                ('create_date', models.DateTimeField(auto_now_add=True)),
                (
                    'feed',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to='HallowWatch.feed',
                    ),
                ),
                (
                    'source',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to='HallowWatch.source',
                    ),
                ),
                (
                    'tag',
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to='HallowWatch.tag',
                    ),
                ),
            ],
            options={
                'ordering': ['-create_date'],
            },
        ),
    ]
