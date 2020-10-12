from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render
from football.models import LeagueSettings as FootballLeagueSettings
from operator import attrgetter

def index(request):
    
    # league_settings = FootballLeagueSettings.objects.filter(owner=request.user)
    all_sheets = FootballLeagueSettings.objects.all()

    sorted_sheets = sorted(all_sheets, key= attrgetter('id'))

    first_3_sheets = sorted_sheets[:3]

    context = {
        'default_sheets': first_3_sheets
    }

    return render(request, 'base_pages/index.html', context)


def about(request):
    return render(request, 'base_pages/about.html')


@login_required
def dashboard(request):

    league_settings = FootballLeagueSettings.objects.filter(owner=request.user)

    context = {
        'league_settings': league_settings
    }

    return render(request, 'base_pages/dashboard.html', context)
