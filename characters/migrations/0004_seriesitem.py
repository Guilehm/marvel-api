# Generated by Django 2.1.7 on 2019-02-15 23:11

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('characters', '0003_auto_20190215_2259'),
    ]

    operations = [
        migrations.CreateModel(
            name='SeriesItem',
            fields=[
                ('id', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('resource_uri', models.URLField(blank=True, null=True)),
                ('data', django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True)),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('date_changed', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]