from django.db import models

import core.choices as choices_core


class Match(models.Model):
    division = models.ForeignKey('Division', null=True, on_delete=models.SET_NULL)
    date = models.DateField(null=True)
    home_team = models.ForeignKey('Team', null=True, related_name='home_team', on_delete=models.SET_NULL)
    away_team = models.ForeignKey('Team', null=True, related_name='away_team', on_delete=models.SET_NULL)
    ft_home_goals = models.SmallIntegerField(null=False)
    ft_away_goals = models.SmallIntegerField(null=False)
    ft_result = models.SmallIntegerField(choices=choices_core.RESULT, null=False)
    ht_home_goals = models.SmallIntegerField(null=False)
    ht_away_goals = models.SmallIntegerField(null=False)
    ht_result = models.SmallIntegerField(choices=choices_core.RESULT, null=False)
    odds_home = models.FloatField(null=True)
    odds_draw = models.FloatField(null=True)
    odds_away = models.FloatField(null=True)

    class Meta:
        verbose_name_plural = "matches"

    def __str__(self):
        return '{} - {} on {}'.format(self.home_team, self.away_team, self.date)


class Team(models.Model):
    name = models.CharField(max_length=100, blank=True)
    division = models.ForeignKey('Division', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return str(self.name)


class Division(models.Model):
    name = models.IntegerField(choices=choices_core.LEAGUES)

    def __str__(self):
        return str(self.get_name_display())