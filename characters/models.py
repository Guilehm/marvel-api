from django.contrib.postgres.fields import JSONField
from django.db import models

from marvel.settings import BASE_URL


class Character(models.Model):
    id = models.CharField(primary_key=True, max_length=50)
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    resource_uri = models.URLField(null=True, blank=True)
    data = JSONField(null=True, blank=True)
    comics = models.ManyToManyField(
        'characters.Comic',
        related_name='characters',
        blank=True,
        through='CharacterComic',
        through_fields=('character', 'comic')
    )
    series = models.ManyToManyField(
        'characters.Series',
        related_name='characters',
        blank=True,
        through='CharacterSeries',
        through_fields=('character', 'series')
    )
    events = models.ManyToManyField(
        'characters.Event',
        related_name='characters',
        blank=True,
        through='CharacterEvent',
        through_fields=('character', 'event')
    )
    stories = models.ManyToManyField(
        'characters.Story',
        related_name='characters',
        blank=True,
        through='CharacterStory',
        through_fields=('character', 'story')
    )

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


class CharacterComic(models.Model):
    character = models.ForeignKey('characters.Character', on_delete=models.CASCADE)
    comic = models.ForeignKey('characters.Comic', on_delete=models.CASCADE)

    date_added = models.DateTimeField(auto_now_add=True)
    date_changed = models.DateTimeField(auto_now=True)


class CharacterSeries(models.Model):
    character = models.ForeignKey('characters.Character', on_delete=models.CASCADE)
    series = models.ForeignKey('characters.Series', on_delete=models.CASCADE)

    date_added = models.DateTimeField(auto_now_add=True)
    date_changed = models.DateTimeField(auto_now=True)


class CharacterEvent(models.Model):
    character = models.ForeignKey('characters.Character', on_delete=models.CASCADE)
    event = models.ForeignKey('characters.Event', on_delete=models.CASCADE)

    date_added = models.DateTimeField(auto_now_add=True)
    date_changed = models.DateTimeField(auto_now=True)


class CharacterStory(models.Model):
    character = models.ForeignKey('characters.Character', on_delete=models.CASCADE)
    story = models.ForeignKey('characters.Story', on_delete=models.CASCADE)

    date_added = models.DateTimeField(auto_now_add=True)
    date_changed = models.DateTimeField(auto_now=True)


class Comic(models.Model):
    id = models.CharField(primary_key=True, max_length=50)
    name = models.CharField(max_length=255)
    resource_uri = models.URLField(null=True, blank=True)
    data = JSONField(null=True, blank=True)

    date_added = models.DateTimeField(auto_now_add=True)
    date_changed = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.name}'


class Series(models.Model):
    id = models.CharField(primary_key=True, max_length=50)
    name = models.CharField(max_length=255)
    resource_uri = models.URLField(null=True, blank=True)
    data = JSONField(null=True, blank=True)

    date_added = models.DateTimeField(auto_now_add=True)
    date_changed = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name_plural = 'series'


class Event(models.Model):
    id = models.CharField(primary_key=True, max_length=50)
    name = models.CharField(max_length=255)
    resource_uri = models.URLField(null=True, blank=True)
    data = JSONField(null=True, blank=True)

    date_added = models.DateTimeField(auto_now_add=True)
    date_changed = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.name}'


class Story(models.Model):
    id = models.CharField(primary_key=True, max_length=50)
    name = models.CharField(max_length=255)
    type = models.CharField(max_length=255)
    resource_uri = models.URLField(null=True, blank=True)
    data = JSONField(null=True, blank=True)

    date_added = models.DateTimeField(auto_now_add=True)
    date_changed = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.name}'
