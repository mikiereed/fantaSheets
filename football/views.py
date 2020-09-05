from django.shortcuts import render


def index(request):
    return render(request, 'football/fantaSheets.html')


def fantaSheet(request):
    return render(request, 'football/fantaSheet.html')
