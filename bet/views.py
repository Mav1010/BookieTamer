from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView

from django_filters.views import FilterView 

from .models import Bet


class BetList(FilterView):
    model = Bet
    context_object_name = 'match'
    template_name = 'analysis/data.html'