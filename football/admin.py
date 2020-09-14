from django.contrib import admin
from .models import LeagueSettings


@admin.register(LeagueSettings)
class LeagueSettingsAdmin(admin.ModelAdmin):
    list_display = ('owner', 'title', 'league_hosting_site')
