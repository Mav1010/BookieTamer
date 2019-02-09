from django_filters.views import FilterView
from django.shortcuts import render

from analysis.filters import MatchFilter
from core import choices as choices_core
from core.models import Match, Division, Team


class MatchList(FilterView):
    model = Match
    context_object_name = 'match'
    template_name = 'analysis/data.html'
    filterset_class = MatchFilter

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)

        if self.request.GET.get('division'):
            division_list =  self.request.GET.get('division')
        else:
            division_list = Division.objects.all()

        if self.request.GET.get('home_team'):
            home_team = self.request.GET.get('home_team')
        else:
            home_team = Team.objects.all()

        if self.request.GET.get('away_team'):
            away_team = self.request.GET.get('away_team')
        else:
            away_team = Team.objects.all()

        if self.request.GET.get('ft_result'):
            ft_result = self.request.GET.get('ft_result')

        if self.request.GET.get('ht_result'):
            ht_result = self.request.GET.get('ht_result')

        base_filter = Match.objects.filter(division__in=division_list,
                                           home_team__in=home_team,
                                           away_team__in=away_team,
                                           )

        base_filter_count = base_filter.count()

        home_wins = base_filter.filter(ft_result=choices_core.HOME_WIN).count()
        away_wins = base_filter.filter(ft_result=choices_core.AWAY_WIN).count()
        draws = base_filter.filter(ft_result=choices_core.DRAW).count()

        context['division_list'] = division_list
        context['home_team'] = home_team
        context['away_team'] = away_team
        context['base_filter_count'] = base_filter_count

        try:
            context['home_wins_percentage'] = home_wins / base_filter_count
        except:
            context['home_wins_percentage'] = 0

        try:
            context['away_wins_percentage'] = away_wins / base_filter_count
        except:
            context['away_wins_percentage'] = 0

        try:
            context['draws_percentage'] = draws / base_filter_count
        except:
            context['draws_percentage'] = 0

        return context


def ajax_load_teams_by_division(request):
    division_id = request.GET.get('division_id')
    try:
        division = Division.objects.get(name=division_id)
        teams_qs = Team.objects.filter(division=division)
    except (Division.DoesNotExist, ValueError):
        division = Division.objects.all()
        teams_qs = Team.objects.filter(division__in=division)

    return render(request, 'analysis/team_choice.html', {'teams': teams_qs})


