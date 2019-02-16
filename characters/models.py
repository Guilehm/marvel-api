from django.contrib.postgres.fields import JSONField
from django.db import models

from marvel.settings import BASE_URL


class Character(models.Model):
    id = models.CharField(primary_key=True, max_length=50)
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    resource_uri = models.URLField(null=True, blank=True)
    data = JSONField(null=True, blank=True)
    comics = models.ManyToManyField('characters.ComicItem', related_name='characters', blank=True)
    series = models.ManyToManyField('characters.SeriesItem', related_name='characters', blank=True)
    events = models.ManyToManyField('characters.EventItem', related_name='characters', blank=True)
    stories = models.ManyToManyField('characters.StoryItem', related_name='characters', blank=True)

    date_added = models.DateTimeField(auto_now_add=True)
    date_changed = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.name}'

    def get_resource_uri(self, resource_name, api_version='v1'):
        base_url = BASE_URL.format(api_version=api_version)
        return f'{base_url}characters/{self.id}/{resource_name}'

    @property
    def thumbnail_url(self):
        try:
            thumb = self.data['thumbnail']
            path, extension = thumb.values()
            filename = path.rpartition('/')[-1]
            if filename != 'image_not_available':
                return f"{path}.{extension}"
        except (IndexError, TypeError):
            return


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
