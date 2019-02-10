from django.db.models import Avg
from django.shortcuts import render

from django_filters.views import FilterView

from analysis.filters import MatchFilter
from analysis.utils import divide_without_errors, color_if_higher_lower
from core import choices as choices_core
from core.models import Match, Division, Team


class MatchList(FilterView):
    model = Match
    context_object_name = 'match'
    template_name = 'analysis/data.html'
    filterset_class = MatchFilter
    paginate_by = 30

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)

        # calculate statistics data
        qs = self.object_list
        num_games = len(qs)

        # full time result percentages
        home_win_count = qs.filter(ft_result=choices_core.HOME_WIN).count()
        draw_count = qs.filter(ft_result=choices_core.DRAW).count()
        away_win_count = qs.filter(ft_result=choices_core.AWAY_WIN).count()

        home_win_percentage = divide_without_errors(home_win_count, num_games)
        draw_percentage = divide_without_errors(draw_count, num_games)
        away_win_percentage = divide_without_errors(away_win_count, num_games)

        context['home_win_percentage'] = home_win_percentage
        context['draw_percentage'] = draw_percentage
        context['away_win_percentage'] = away_win_percentage

        # avg. goals
        avg_ft_home_goals = qs.all().aggregate(Avg('ft_home_goals'))['ft_home_goals__avg']
        avg_ft_away_goals = qs.all().aggregate(Avg('ft_away_goals'))['ft_away_goals__avg']

        context['avg_ft_home_goals'] = avg_ft_home_goals
        context['avg_ft_away_goals'] = avg_ft_away_goals

        # avg. odds
        avg_home_odds = qs.all().aggregate(Avg('odds_home'))['odds_home__avg']
        avg_draw_odds = qs.all().aggregate(Avg('odds_draw'))['odds_draw__avg']
        avg_away_odds = qs.all().aggregate(Avg('odds_away'))['odds_away__avg']

        context['avg_home_odds'] = avg_home_odds
        context['avg_draw_odds'] = avg_draw_odds
        context['avg_away_odds'] = avg_away_odds

        bookie_probability_home = 1/ avg_home_odds
        bookie_probability_draw = 1/ avg_draw_odds
        bookie_probability_away = 1/ avg_away_odds

        context['bookie_probability_home'] = bookie_probability_home
        context['bookie_probability_draw'] = bookie_probability_draw
        context['bookie_probability_away'] = bookie_probability_away

        # color code for values
        home_win_color = color_if_higher_lower(home_win_percentage, bookie_probability_home)
        draw_color = color_if_higher_lower(draw_percentage, bookie_probability_draw)
        away_win_color = color_if_higher_lower(away_win_percentage, bookie_probability_away)

        context['home_win_color'] = home_win_color
        context['draw_color'] = draw_color
        context['away_win_color'] = away_win_color

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


