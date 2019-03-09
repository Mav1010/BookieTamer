from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views.generic import UpdateView, CreateView

from datafetch.forms import DataFetchSettingsForm
from datafetch.models import DataFetchSettings
from datafetch.utils import get_fortuna_games


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
    template_name = 'core/base_add_update.html'
    form_class = DataFetchSettingsForm

    def dispatch(self, request, *args, **kwargs):
        try:
            settings = DataFetchSettings.objects.get(user=self.request.user)
            return redirect('datafetch:datafetch_settings', settings.pk)
        except DataFetchSettings.DoesNotExist:
            pass
        return super(DataFetchSettingsCreateView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(DataFetchSettingsCreateView, self).form_valid(form)


class DataFetchSettingsUpdateView(LoginRequiredMixin, UpdateView):
    model = DataFetchSettings
    template_name = 'core/base_add_update.html'
    form_class = DataFetchSettingsForm
