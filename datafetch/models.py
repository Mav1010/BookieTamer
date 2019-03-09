from django.db import models
from django.core.exceptions import ValidationError
from django.shortcuts import reverse


from core.models import BaseModel


class DataFetchSettings(BaseModel):
    difference_x_range_min = models.FloatField(default=0,null=False)
    difference_x_range_max = models.FloatField(default=0,null=False)
    odds_1_min = models.FloatField(default=0, null=False)
    odds_1_max = models.FloatField(default=0, null=False)
    date_offset = models.IntegerField(default=7, null=False)
    odds_1_min_second = models.FloatField(default=0, null=False)
    odds_1_max_second = models.FloatField(default=0, null=False)

    user = models.OneToOneField('users.CustomUser', related_name='user_settings', on_delete=models.CASCADE)

    # def save(self, *args, **kwargs):
    #     if DataFetchSettings.objects.filter().exists():
    #         raise ValidationError('You cannot have multiple settings')
    #
    #     return super(DataFetchSettings, self).save(*args,1 **kwargs)

    def get_absolute_url(self):
        return reverse('datafetch:datafetch_settings', kwargs={'pk': self.pk })