from django.db import models
from django.shortcuts import reverse

from core.models import BaseModel


class DataFetchSettings(BaseModel):
    name = models.CharField(max_length=256, blank=True)
    difference_x_range_min = models.FloatField(null=True, blank=True)
    difference_x_range_max = models.FloatField(null=True, blank=True)
    odds_1_min = models.FloatField(null=True, blank=True)
    odds_1_max = models.FloatField(null=True, blank=True)
    odds_2_min = models.FloatField(null=True, blank=True)
    odds_2_max = models.FloatField(null=True, blank=True)
    date_offset = models.IntegerField(default=7, null=False)

    user = models.ForeignKey('users.CustomUser', related_name='user_settings', on_delete=models.CASCADE)
    leagues = models.ManyToManyField('core.Division', related_name='leagues', blank=True)

    def get_absolute_url(self):
        return reverse('datafetch:datafetch_settings_update', kwargs={'pk': self.pk })