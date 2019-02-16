from django.contrib import admin

from characters.models import Character, ComicItem, EventItem, SeriesItem, StoryItem


class CharacterComicItemInline(admin.StackedInline):
    model = ComicItem.characters.through
    raw_id_fields = ('comicitem',)
    extra = 0


class CharacterSeriesItemInline(admin.StackedInline):
    model = SeriesItem.characters.through
    raw_id_fields = ('seriesitem',)
    extra = 0


class CharacterEventsItemInline(admin.StackedInline):
    model = EventItem.characters.through
    raw_id_fields = ('eventitem',)
    extra = 0


class CharacterStoriesItemInline(admin.StackedInline):
    model = StoryItem.characters.through
    raw_id_fields = ('storyitem',)
    extra = 0


@admin.register(Character)
class CharacterAdmin(admin.ModelAdmin):
    list_display = ('id', 'name',)
    list_filter = ('date_added', 'date_changed')
    search_fields = ('id', 'name', 'resource_uri')
    exclude = ('comics', 'series', 'events', 'stories')
    inlines = (
        CharacterComicItemInline,
        CharacterSeriesItemInline,
        CharacterEventsItemInline,
        CharacterStoriesItemInline,
    )


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


@admin.register(EventItem)
class EventItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'name',)
    list_filter = ('date_added', 'date_changed')
    search_fields = ('id', 'name', 'resource_uri')


@admin.register(StoryItem)
class StoryItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'type')
    list_filter = ('type', 'date_added', 'date_changed')
    search_fields = ('id', 'name', 'resource_uri')
