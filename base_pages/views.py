from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render
from football.models import LeagueSettings as FootballLeagueSettings


def index(request):
    return render(request, 'base_pages/index.html')


def about(request):
    return render(request, 'base_pages/about.html')


@login_required
def dashboard(request):
    fantaSheets = FootballLeagueSettings.objects.filter(owner=request.user)

    context = {
        'fantaSheets': fantaSheets
    }

    return render(request, 'base_pages/dashboard.html', context)
