from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView

from django_filters.views import FilterView 

from .models import Bet


class BetList(LoginRequiredMixin, FilterView):
    model = Bet
    context_object_name = 'match'
    template_name = 'analysis/data.html'