from django.db import models

from core import choices as choices_core
from core.models import BaseMatch, Team, Division


class Bet(BaseMatch):
    budget = models.IntegerField(default=0, null=True)
    home_team = models.ForeignKey('core.Team', null=True, related_name='bet_home_team', on_delete=models.SET_NULL)
    away_team = models.ForeignKey('core.Team', null=True, related_name='bet_away_team', on_delete=models.SET_NULL)
    division = models.ForeignKey('core.Division', related_name='bet_division', null=True, on_delete=models.SET_NULL)
    betted_outcome = models.CharField(max_length=1, choices=choices_core.RESULT, blank=True)
    stake = models.IntegerField(default=0, null=True)
    result = models.CharField(max_length=1, choices=choices_core.RESULT, blank=True)
    success = models.BooleanField()
