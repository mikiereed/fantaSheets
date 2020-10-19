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
            print('yay')
        else:
            print(league_settings_form.errors)
            # messages.error(request, league_settings_form.errors)

    print('quarterbacks', league_settings_form['roster_quarterbacks'].value())
    print('running backs', league_settings_form['roster_running_backs'].value())
    print('wide receivers', league_settings_form['roster_wide_receivers'].value())
    print('tight_ends', league_settings_form['roster_tight_ends'].value())
    print('offensive_players', league_settings_form['roster_offensive_players'].value())

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
            __set_roster_nulls_to_zero(new_settings)
            new_settings.save()
            messages.success(request, 'fantaSheet Settings Saved')
            return redirect('dashboard')
        else:
            messages.error(request, league_settings_form.errors)
    else:
        league_settings_form = LeagueSettingsForm(use_required_attribute=False)
    return render(request, 'football/create.html',
                  {'league_settings_form': league_settings_form})

def __set_roster_nulls_to_zero(settings_list):

    settings_list_attributes = [attr for attr in dir(settings_list) if attr.startswith('roster_')]
    print(settings_list_attributes)
    for attribute in settings_list_attributes:
        setting_value = getattr(settings_list, attribute)
        if (setting_value is None):
            setattr(
                settings_list,
                attribute,
                0
            )
    