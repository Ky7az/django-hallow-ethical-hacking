# Generated by Django 3.2.19 on 2023-07-12 13:13

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('HallowWatch', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='feed',
            name='source',
            field=models.OneToOneField(
                on_delete=django.db.models.deletion.CASCADE, to='HallowWatch.source'
            ),
        ),
    ]
