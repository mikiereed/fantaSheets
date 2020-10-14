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
        else:
            print(league_settings_form.errors)
            # messages.error(request, league_settings_form.errors)

    print('quarterbacks', league_settings_form['roster_quarterbacks'].value())

    # league_settings = LeagueSettings()

    # print(league_settings_form)

    return redirect('index')

@login_required
def create(request):
    if request.method == 'POST':
        league_settings_form = LeagueSettingsForm(request.POST)
        if league_settings_form.is_valid():
            new_settings = league_settings_form.save(commit=False)
            new_settings.owner_id = request.POST['owner']
            new_settings.roster_defensive_tackles = 0
            new_settings.roster_defensive_ends = 0
            new_settings.roster_defensive_lines = 0
            new_settings.roster_defensive_players = 0
            new_settings.roster_linebackers = 0
            new_settings.roster_edge_rushers = 0
            new_settings.roster_defensive_backs = 0
            new_settings.roster_cornerbacks = 0
            new_settings.roster_safeties = 0
            new_settings.roster_punters = 0
            new_settings.roster_head_coaches = 0
            new_settings.roster_team_quarterbacks = 0
            new_settings.roster_injured_reserve_spots = 0
            new_settings.save()
            messages.success(request, 'fantaSheet Settings Saved')
            return redirect('dashboard')
        else:
            messages.error(request, league_settings_form.errors)
    else:
        league_settings_form = LeagueSettingsForm(use_required_attribute=False)
    return render(request, 'football/create.html',
                  {'league_settings_form': league_settings_form})
