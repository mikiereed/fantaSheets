from .forms import LeagueSettingsForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.contrib import messages


def index(request):
    return render(request, 'football/fantaSheets.html')


def fantaSheet(request):
    return render(request, 'football/fantaSheet.html')


@login_required
def create(request):
    if request.method == 'POST':
        league_settings_form = LeagueSettingsForm(request.POST)
        if league_settings_form.is_valid():
            # Create a new user object but avoid saving it yet
            new_settings = league_settings_form.save(commit=False)
            # Set the chosen password
            new_settings.owner_id = request.POST['owner']
            # Save the User object
            new_settings.save()
            messages.success(request, 'fantaSheet Settings Saved')
            return render(request, 'base_pages/dashboard.html')
        else:
            messages.error(request, league_settings_form.errors)
    else:
        league_settings_form = LeagueSettingsForm(use_required_attribute=False)
    return render(request, 'football/create.html',
                  {'league_settings_form': league_settings_form})
