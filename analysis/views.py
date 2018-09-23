from django.shortcuts import render
from django_filters.views import FilterView

from analysis.models import Match
from analysis.filters import MatchFilter

def home(request):
    context = {}

    return render(request, 'analysis/pages/home.html', context)

class MatchList(FilterView):
    model = Match
    context_object_name = 'match'
    template_name = 'analysis/pages/data.html'
    filterset_class = MatchFilter