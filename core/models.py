from django.db import models

import core.choices as choices_core


""" base model for all models in the application """
class BaseModel(models.Model):
    date_created = models.DateTimeField(auto_now_add=True)
    date_changed = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class BaseMatch(BaseModel):
    date = models.DateField(null=True)
    ft_result = models.CharField(max_length=1, choices=choices_core.RESULT, blank=False)
    odds_home = models.FloatField(null=True)
    odds_draw = models.FloatField(null=True)
    odds_away = models.FloatField(null=True)

    class Meta:
        abstract = True


class Match(BaseMatch):
    home_team = models.ForeignKey('core.Team', null=True, related_name='home_team', on_delete=models.SET_NULL)
    away_team = models.ForeignKey('core.Team', null=True, related_name='away_team', on_delete=models.SET_NULL)
    division = models.ForeignKey('core.Division', null=True, on_delete=models.SET_NULL)
    ft_home_goals = models.SmallIntegerField(null=False)
    ft_away_goals = models.SmallIntegerField(null=False)
    ht_home_goals = models.SmallIntegerField(null=False)
    ht_away_goals = models.SmallIntegerField(null=False)
    ht_result = models.CharField(max_length=1, choices=choices_core.RESULT, blank=False)

    class Meta:
        verbose_name_plural = "matches"
        ordering = ['-date']

    def __str__(self):
        return '{} - {} on {}'.format(self.home_team, self.away_team, self.date)


class Team(BaseModel):
    name = models.CharField(max_length=100, blank=True)
    division = models.ForeignKey('core.Division', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return str(self.name)


class Division(BaseModel):
    name = models.CharField(max_length=50, blank=False)
    fortuna_url = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return str(self.name)