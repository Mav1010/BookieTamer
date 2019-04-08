from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, Http404
from django.views.generic import UpdateView, CreateView, ListView

from datafetch.forms import DataFetchSettingsForm
from datafetch.models import DataFetchSettings
from datafetch.utils import get_fortuna_games

from users.models import CustomUser


@login_required
def games_to_bet_list(request):
    try:
        fetch_settings = DataFetchSettings.objects.get(user=request.user)
        df = get_fortuna_games(fetch_settings)
        html_table = df.sort_values(by=['Match Day', 'X coef']).to_html(index=False)

        context = {
            'html_table': html_table,
        }
    except DataFetchSettings.DoesNotExist:
        no_settings = True
        context = {
            'no_settings': no_settings,
        }
    return render(request, 'datafetch/games_to_bet.html', context)


class DataFetchSettingsList(ListView):
    model = DataFetchSettings
    template_name = 'datafetch/datafetch_list.html'
    context_object_name = 'settings'

    def dispatch(self, request, *args, **kwargs):
        try:
            settings = DataFetchSettings.objects.filter(user=self.request.user)
            print(settings)
            return super(DataFetchSettingsList, self).dispatch(request, *args, **kwargs)
        except DataFetchSettings.DoesNotExist:
            return redirect('datafetch:datafetch_settings_create')


    def get_context_data(self, **kwargs):
        context = super(DataFetchSettingsList, self).get_context_data(**kwargs)
        try:
            user = CustomUser.objects.get(id=self.request.user.id)
        except CustomUser.DoesNotExist:
            user = None

        context['settings'] = user.user_settings
        context.update({
            'title': 'Settings'
        })

        return context


class DataFetchSettingsCreate(LoginRequiredMixin, CreateView):
    model = DataFetchSettings
    template_name = 'core/base_add_update.html'
    form_class = DataFetchSettingsForm

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(DataFetchSettingsCreate, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(DataFetchSettingsCreate, self).get_context_data(**kwargs)
        context.update({'title': 'Settings'})
        return context


class DataFetchSettingsUpdate(LoginRequiredMixin, UpdateView):
    model = DataFetchSettings
    template_name = 'core/base_add_update.html'
    form_class = DataFetchSettingsForm

    def get_context_data(self, **kwargs):
        context = super(DataFetchSettingsUpdate, self).get_context_data(**kwargs)
        context.update({'title': 'Settings'})
        return context
