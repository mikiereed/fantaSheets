from import_export.admin import ImportExportModelAdmin
from django.contrib import admin
from .models import LeagueSettings, Position, Projections, Team


@admin.register(LeagueSettings)
class LeagueSettingsAdmin(admin.ModelAdmin):
    list_display = ('id', 'owner', 'title', 'league_hosting_site')
    list_display_links = ('id', 'title')
    list_filter = ('owner', 'league_hosting_site')
    search_fields = ('owner', 'title')
    list_per_page = 100
    # list_editable = ('league_hosting_site',)


@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'abbreviation')
    list_display_links = ('id', 'name', 'abbreviation')


@admin.register(Projections)
class ProjectionsAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('id', 'player', 'team', 'position',)
    list_display_links = ('id', 'player',)
    list_filter = ('team', 'position',)
    search_fields = ('player', 'team', 'position',)
    list_per_page = 100


@admin.register(Team)
class TeamAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('id', 'abbreviation', 'city', 'mascot', 'bye_week',)
    list_display_links = ('id', 'abbreviation', 'city', 'mascot',)
    list_per_page = 40