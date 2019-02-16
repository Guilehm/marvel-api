from django.contrib.postgres.fields import JSONField
from django.db import models


class Character(models.Model):
    id = models.CharField(primary_key=True, max_length=50)
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    resource_uri = models.URLField(null=True, blank=True)
    data = JSONField(null=True, blank=True)
    comics = models.ManyToManyField('characters.ComicItem', related_name='comics')
    series = models.ManyToManyField('characters.SeriesItem', related_name='series')
    events = models.ManyToManyField('characters.EventItem', related_name='events')
    stories = models.ManyToManyField('characters.StoryItem', related_name='stories')

    comics_resource_uri = models.URLField(null=True, blank=True)
    series_resource_uri = models.URLField(null=True, blank=True)
    stories_resource_uri = models.URLField(null=True, blank=True)
    events_resource_uri = models.URLField(null=True, blank=True)

    date_added = models.DateTimeField(auto_now_add=True)
    date_changed = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.name}'


class ComicItem(models.Model):
    id = models.CharField(primary_key=True, max_length=50)
    name = models.CharField(max_length=255)
    resource_uri = models.URLField(null=True, blank=True)
    data = JSONField(null=True, blank=True)

    date_added = models.DateTimeField(auto_now_add=True)
    date_changed = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.name}'


class SeriesItem(models.Model):
    id = models.CharField(primary_key=True, max_length=50)
    name = models.CharField(max_length=255)
    resource_uri = models.URLField(null=True, blank=True)
    data = JSONField(null=True, blank=True)

    date_added = models.DateTimeField(auto_now_add=True)
    date_changed = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.name}'


class EventItem(models.Model):
    id = models.CharField(primary_key=True, max_length=50)
    name = models.CharField(max_length=255)
    resource_uri = models.URLField(null=True, blank=True)
    data = JSONField(null=True, blank=True)

    date_added = models.DateTimeField(auto_now_add=True)
    date_changed = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.name}'


class StoryItem(models.Model):
    id = models.CharField(primary_key=True, max_length=50)
    name = models.CharField(max_length=255)
    type = models.CharField(max_length=255)
    resource_uri = models.URLField(null=True, blank=True)
    data = JSONField(null=True, blank=True)

    date_added = models.DateTimeField(auto_now_add=True)
    date_changed = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.name}'
