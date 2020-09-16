from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    return render(request, 'base_pages/index.html')


def about(request):
    return render(request, 'base_pages/about.html')


def dashboard(request):
    return render(request, 'base_pages/dashboard.html')
