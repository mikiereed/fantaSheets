from .forms import LeagueSettingsForm, AnonymousLeagueSettingsForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import LeagueSettings
from .services import calculate_fantaSheet


def index(request):
    return render(request, 'football/fantaSheets.html')

def fantaSheet(request, fantaSheet_id):
    league_settings = LeagueSettings.objects.only('id').get(id=fantaSheet_id)

    fantaSheet_values = calculate_fantaSheet(league_settings)

    context = {
        'fantaSheet_values': fantaSheet_values,
        'league_settings' : league_settings,
    }

    return render(request, 'football/fantaSheet.html', context)

def anonymous_fantaSheet(request):

    if request.method == 'POST':
        league_settings_form = AnonymousLeagueSettingsForm(request.POST)
        if league_settings_form.is_valid():
            clean_settings = league_settings_form.save(commit=False)
            __set_default_settings(clean_settings)
            __set_all_nulls_to_zero(clean_settings)
            clean_settings.save()
            return redirect('fantaSheet', fantaSheet_id=clean_settings.id)
        else:
            messages.error(request, league_settings_form.errors)

    return redirect('index')

@login_required
def create(request):
    if request.method == 'POST':
        league_settings_form = LeagueSettingsForm(request.POST)
        if league_settings_form.is_valid():
            new_settings = league_settings_form.save(commit=False)
            new_settings.owner_id = request.POST['owner']
            __set_all_nulls_to_zero(new_settings)
            new_settings.save()
            messages.success(request, 'fantaSheet Settings Saved')
            return redirect('dashboard')
        else:
            messages.error(request, league_settings_form.errors)
    else:
        league_settings_form = LeagueSettingsForm(use_required_attribute=False)
    return render(request, 'football/create.html',
                  {'league_settings_form': league_settings_form})

def __set_all_nulls_to_zero(settings_list):
    
    __set_setting_by_type_to_null(starts_with='roster_', settings_list=settings_list)
    __set_setting_by_type_to_null(starts_with='passing_', settings_list=settings_list)
    __set_setting_by_type_to_null(starts_with='rushing_', settings_list=settings_list)
    __set_setting_by_type_to_null(starts_with='receiving_', settings_list=settings_list)
    __set_setting_by_type_to_null(starts_with='kicking_', settings_list=settings_list)
    __set_setting_by_type_to_null(starts_with='individual_', settings_list=settings_list)
    __set_setting_by_type_to_null(starts_with='dst_', settings_list=settings_list)

def __set_default_settings(settings_list):

    default_league_settings = LeagueSettings.objects.only('id').get(id=1) # id 1 is the ESPN defaults

    # save settings prior to setting all to defaults, reset after
    user_passing_touchdown_value = settings_list.passing_touchdowns
    user_receiving_receptions = settings_list.receiving_receptions

    __set_settings_from_default(settings_list, default_league_settings, 'passing_')
    __set_settings_from_default(settings_list, default_league_settings, 'rushing_')
    __set_settings_from_default(settings_list, default_league_settings, 'receiving_')
    __set_settings_from_default(settings_list, default_league_settings, 'individual_')
    __set_settings_from_default(settings_list, default_league_settings, 'kicking_')
    __set_settings_from_default(settings_list, default_league_settings, 'dst_')

    # reset after default is set
    settings_list.passing_touchdowns = user_passing_touchdown_value
    settings_list.receiving_receptions = user_receiving_receptions

    settings_list.title = 'Simple FantaSheet'
    settings_list.league_hosting_site = 'other'
    settings_list.roster_team_defense_special_teams = getattr(default_league_settings, 'roster_team_defense_special_teams')
    settings_list.roster_kickers = getattr(default_league_settings, 'roster_kickers')
    settings_list.roster_bench_spots = getattr(default_league_settings, 'roster_bench_spots')

def __set_setting_by_type_to_null(starts_with, settings_list):

    settings_list_attributes = [attr for attr in dir(settings_list) if attr.startswith(starts_with)]
    for attribute in settings_list_attributes:
        setting_value = getattr(settings_list, attribute)
        if (setting_value is None):
            setattr(
                settings_list,
                attribute,
                0
            )

def __set_settings_from_default(settings_list, default_league_settings, setting_starts_with):

    settings_list_attributes = [attr for attr in dir(settings_list) if attr.startswith(setting_starts_with)]
    for attribute in settings_list_attributes:
        default_setting_value = getattr(default_league_settings, attribute)
        setattr(
            settings_list,
            attribute,
            default_setting_value
        )