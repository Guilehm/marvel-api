from django.contrib import admin

from characters.models import Character


@admin.register(Character)
class CharacterAdmin(admin.ModelAdmin):
    list_display = ('name',)
    list_filter = ('date_added', 'date_changed')
    search_fields = ('name', 'resource_uri')
