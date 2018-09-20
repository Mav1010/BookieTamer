from django.shortcuts import render
from analysis.models import Match


def home(request):

    matches = Match.objects.all()

    context = {
        'matches': matches,
    }

    return render(request, 'analysis/pages/blank.html', context)