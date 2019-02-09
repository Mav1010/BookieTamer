from django.db import models
from django.core.exceptions import ValidationError


class DataFetchSettings(models.Model):

    difference_x_range_min = models.FloatField(default=0,null=False)
    difference_x_range_max = models.FloatField(default=0,null=False)
    odds_1_min = models.FloatField(default=0, null=False)
    odds_1_max = models.FloatField(default=0, null=False)
    date_offset = models.IntegerField(default=7, null=False)
    odds_1_min_second = models.FloatField(default=0, null=False)
    odds_1_max_second = models.FloatField(default=0, null=False)

    def save(self, *args, **kwargs):
        if DataFetchSettings.objects.exists() and not self.pk:
            raise ValidationError('You cannot have multiple settings')

        return super(DataFetchSettings, self).save(*args, **kwargs)