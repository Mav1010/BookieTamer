import django_filters

from django import forms

from analysis.utils import get_real_h_a_odds_difference
from core import choices as choices
from core.models import Match, Team, Division
from datafetch.models import DataFetchSettings


def division_choices():
    divisions = Division.objects.all()
    choices_leagues = tuple((division.id, division.name) for division in divisions)
    return choices_leagues


class MatchFilter(django_filters.FilterSet):

    division = django_filters.MultipleChoiceFilter(choices=division_choices(),
                                                   widget=forms.SelectMultiple(attrs={'class':'form-control js-multiple-select2'}))

    home_team = django_filters.ModelChoiceFilter(widget=forms.Select(attrs={'class':'form-control team-selection'}),
                                                 queryset=Team.objects.all())

    away_team = django_filters.ModelChoiceFilter(widget=forms.Select(attrs={'class':'form-control team-selection'}),
                                                 queryset=Team.objects.all())


    ft_result = django_filters.ChoiceFilter(choices=choices.RESULT,
                                            widget = forms.Select(attrs={'class': 'form-control'}))

    ht_result = django_filters.ChoiceFilter(choices=choices.RESULT,
                                            widget=forms.Select(attrs={'class': 'form-control'}))

    start_date = django_filters.DateFilter(field_name='date',
                                           lookup_expr=('gte'),
                                           widget=forms.DateInput(attrs={'class': 'form-control',
                                                                         'type': 'date'}))

    end_date = django_filters.DateFilter(field_name='date',
                                         lookup_expr=('lte'),
                                         widget=forms.DateInput(attrs={'class': 'form-control',
                                                                       'type': 'date'}))

    ft_home_goals_from = django_filters.NumberFilter(field_name='ft_home_goals',
                                                     lookup_expr=('gte'))
    ft_home_goals_to = django_filters.NumberFilter(field_name='ft_home_goals',
                                                   lookup_expr=('lte'))

    ft_away_goals_from = django_filters.NumberFilter(field_name='ft_away_goals',
                                                     lookup_expr=('gte'))
    ft_away_goals_to = django_filters.NumberFilter(field_name='ft_away_goals',
                                                   lookup_expr=('lte'))

    odds_home_from = django_filters.NumberFilter(field_name='odds_home',
                                                 lookup_expr=('gte'))

    odds_home_to = django_filters.NumberFilter(field_name='odds_home',
                                               lookup_expr=('lte'))

    odds_draw_from = django_filters.NumberFilter(field_name='odds_draw',
                                                 lookup_expr=('gte'))

    odds_draw_to = django_filters.NumberFilter(field_name='odds_draw',
                                               lookup_expr=('lte'))

    odds_away_from = django_filters.NumberFilter(field_name='odds_away',
                                                 lookup_expr=('gte'))

    odds_away_to = django_filters.NumberFilter(field_name='odds_away',
                                               lookup_expr=('lte'))


    show_matching_current_draw = django_filters.ChoiceFilter(choices=choices.YES_FILTER,
                                                             method='look_by_matching_draw_settings')

    order_by = django_filters.OrderingFilter(
        fields=(
            ('date', 'date'),
            ('odds_home', 'odds_home'),
            ('odds_draw', 'odds_draw'),
            ('odds_away', 'odds_away'),
        ),
    )

    class Meta:
        model = Match
        fields = ['division',
                  'home_team',
                  'away_team',
                  'ft_result',
                  'ht_result',
                  'start_date',
                  'end_date',
                  'ft_home_goals_from',
                  'ft_home_goals_to',
                  'ft_away_goals_from',
                  'ft_away_goals_to',
                  'odds_home_from',
                  'odds_home_to',
                  'odds_draw_from',
                  'odds_draw_to',
                  'odds_away_from',
                  'odds_away_to']


    def look_by_home_team(self, queryset, name, value):
        qs = queryset.filter(home_team=name)
        return qs

    def look_by_away_team(self, queryset, name, value):
        qs = queryset.filter(away_team=name)
        return qs

    def look_by_matching_draw_settings(self, queryset, name, value):

        datafetch_settings = DataFetchSettings.objects.get(user=self.request.user)

        qs = queryset
        wanted = []
        for game in qs:
            difference = get_real_h_a_odds_difference(game.odds_home, game.odds_draw, game.odds_away, datafetch_settings)
            if difference:
                wanted.append(game.pk)

        qs = qs.filter(pk__in=wanted)
        return qs

