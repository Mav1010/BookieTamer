from django.shortcuts import render_to_response
from django.views.generic import UpdateView
from django import forms

from datafetch.models import DataFetchSettings
from datafetch.utils import get_fortuna_games

def games_to_bet_list(request):

    df = get_fortuna_games()
    html_table = df.sort_values('Match Day').to_html(index=False)

    return render_to_response('datafetch/games_to_bet.html', {'html_table': html_table})


class DataFetchSettingsUpdateView(UpdateView):
    model = DataFetchSettings
    fields = ['date_offset',
              'difference_x_range_min',
              'difference_x_range_max',
              'odds_1_min',
              'odds_1_max',
              ]
    template_name = 'datafetch/settings_form.html'
    success_url = '/settings/1'
    widgets = {
        'date_offset': forms.NumberInput(attrs={'class': 'col-sm-4'}),
        'difference_x_range_min': forms.NumberInput(attrs={'class': 'col-sm-4'}),
        'difference_x_range_max': forms.NumberInput(attrs={'class': 'col-sm-4'}),
        'odds_1_min': forms.NumberInput(attrs={'class': 'col-sm-4'}),
        'odds_1_max': forms.NumberInput(attrs={'class': 'col-sm-4'}),
    }