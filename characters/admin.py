from django.contrib import admin

from characters.models import Character, ComicItem, SeriesItem, StoryItem


@admin.register(Character)
class CharacterAdmin(admin.ModelAdmin):
    list_display = ('id', 'name',)
    list_filter = ('date_added', 'date_changed')
    search_fields = ('id', 'name', 'resource_uri')


@admin.register(ComicItem)
class ComicItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'name',)
    list_filter = ('date_added', 'date_changed')
    search_fields = ('id', 'name', 'resource_uri')


@admin.register(SeriesItem)
class SeriesItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'name',)
    list_filter = ('date_added', 'date_changed')
    search_fields = ('id', 'name', 'resource_uri')


@admin.register(StoryItem)
class StoryItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'type')
    list_filter = ('type', 'date_added', 'date_changed')
    search_fields = ('id', 'name', 'resource_uri')
