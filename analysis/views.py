from django.shortcuts import render
from analysis.models import Match


def home(request):

    context = {}

    return render(request, 'analysis/pages/home.html', context)