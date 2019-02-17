from django.contrib import admin

from characters.models import Character, Comic, Event, Series, StoryItem


class CharacterComicInline(admin.TabularInline):
    model = Comic.characters.through
    raw_id_fields = ('comic',)
    classes = ('collapse',)
    extra = 0


class CharacterSeriesInline(admin.TabularInline):
    model = Series.characters.through
    raw_id_fields = ('series',)
    classes = ('collapse',)
    extra = 0


class CharacterEventInline(admin.TabularInline):
    model = Event.characters.through
    raw_id_fields = ('event',)
    classes = ('collapse',)
    extra = 0


class CharacterStoriesItemInline(admin.TabularInline):
    model = StoryItem.characters.through
    raw_id_fields = ('story',)
    classes = ('collapse',)
    extra = 0


@admin.register(Character)
class CharacterAdmin(admin.ModelAdmin):
    list_display = ('id', 'name',)
    list_filter = ('date_added', 'date_changed')
    search_fields = ('id', 'name', 'resource_uri')
    exclude = ('comics', 'series', 'events', 'stories')
    inlines = (
        CharacterComicInline,
        CharacterSeriesInline,
        CharacterEventInline,
        CharacterStoriesItemInline,
    )


@admin.register(Comic)
class ComicAdmin(admin.ModelAdmin):
    list_display = ('id', 'name',)
    list_filter = ('date_added', 'date_changed')
    search_fields = ('id', 'name', 'resource_uri')


@admin.register(Series)
class SeriesItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'name',)
    list_filter = ('date_added', 'date_changed')
    search_fields = ('id', 'name', 'resource_uri')


@admin.register(Event)
class EventItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'name',)
    list_filter = ('date_added', 'date_changed')
    search_fields = ('id', 'name', 'resource_uri')


@admin.register(StoryItem)
class StoryItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'type')
    list_filter = ('type', 'date_added', 'date_changed')
    search_fields = ('id', 'name', 'resource_uri')
