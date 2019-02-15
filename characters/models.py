from django.db import models
from django.contrib.postgres.fields import JSONField


class Character(models.Model):
    id = models.CharField(primary_key=True, max_length=50)
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    resource_uri = models.URLField(null=True, blank=True)
    data = JSONField(null=True, blank=True)

    date_added = models.DateTimeField(auto_now_add=True)
    date_changed = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.name}'
