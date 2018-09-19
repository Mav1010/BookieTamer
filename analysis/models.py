from django.db import models

class Match(models.Model):
    division = models.IntegerField(null=True)
    date = models.DateField(null=True)
    home_team = models.TextField(max_length=50)
    away_team = models.TextField(max_length=50)
    ft_home_goals = models.SmallIntegerField(null=False)
    ft_away_goals = models.SmallIntegerField(null=False)
    ft_result = models.SmallIntegerField(null=False)
    ht_home_goals = models.SmallIntegerField(null=False)
    ht_away_goals = models.SmallIntegerField(null=False)
    ht_result = models.SmallIntegerField(null=False)
    odds_home = models.FloatField(null=True)
    odds_draw = models.FloatField(null=True)
    odds_away = models.FloatField(null=True)

