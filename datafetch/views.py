from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render_to_response
from django.views.generic import UpdateView, CreateView

from datafetch.models import DataFetchSettings
from datafetch.utils import get_fortuna_games


@login_required
def games_to_bet_list(request):

    df = get_fortuna_games()
    html_table = df.sort_values(by=['Match Day', 'X coef']).to_html(index=False)

    return render_to_response('datafetch/games_to_bet.html', {'html_table': html_table})


class DataFetchSettingsCreateView(LoginRequiredMixin, CreateView):
    model = DataFetchSettings
    fields = ['date_offset',
              'difference_x_range_min',
              'difference_x_range_max',
              'odds_1_min',
              'odds_1_max',
              'odds_1_min_second',
              'odds_1_max_second',
              ]
    template_name = 'datafetch/settings_form.html'
    success_url = '/settings/1'


class DataFetchSettingsUpdateView(LoginRequiredMixin, UpdateView):
    model = DataFetchSettings
    fields = ['date_offset',
              'difference_x_range_min',
              'difference_x_range_max',
              'odds_1_min',
              'odds_1_max',
              'odds_1_min_second',
              'odds_1_max_second',
              ]
    template_name = 'datafetch/settings_form.html'
    success_url = '/settings/1'
