from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render_to_response, render, reverse
from django.views.generic import UpdateView, CreateView

from datafetch.forms import DataFetchSettingsForm
from datafetch.models import DataFetchSettings
from datafetch.utils import get_fortuna_games

from users.models import CustomUser


@login_required
def games_to_bet_list(request):
    df = get_fortuna_games()
    html_table = df.sort_values(by=['Match Day', 'X coef']).to_html(index=False)

    context = {
        'html_table': html_table,
    }

    return render(request, 'datafetch/games_to_bet.html', context)


class DataFetchSettingsCreateView(LoginRequiredMixin, CreateView):
    model = DataFetchSettings
    template_name = 'datafetch/settings_form.html'
    form_class = DataFetchSettingsForm

    def get_initial(self):
        inital = {
            'user': self.request.user
        }
        return inital


class DataFetchSettingsUpdateView(LoginRequiredMixin, UpdateView):
    model = DataFetchSettings
    template_name = 'datafetch/settings_form.html'
    form_class = DataFetchSettingsForm

    def get_initial(self):
        inital = {
            'user': self.request.user
        }
        return inital
