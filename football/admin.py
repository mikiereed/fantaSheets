from django.contrib import admin
from .models import LeagueSettings


@admin.register(LeagueSettings)
class LeagueSettingsAdmin(admin.ModelAdmin):
    list_display = ('id', 'owner', 'title', 'league_hosting_site')
    list_display_links = ('id', 'title')
    list_filter = ('owner', 'league_hosting_site')
    search_fields = ('owner', 'title')
    list_per_page = 100
    # list_editable = ('league_hosting_site',)
