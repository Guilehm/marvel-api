from django.db import models


class Character(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=512, null=True, blank=True)
    resource_uri = models.URLField(null=True, blank=True)

    date_added = models.DateTimeField(auto_now_add=True)
    date_changed = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.name}'
