from django import forms

from .models import DataFetchSettings
from core.forms import BootstrapStylingBaseForm


class DataFetchSettingsForm(BootstrapStylingBaseForm, forms.ModelForm):
    field_cols = {
        'date_offset': 2,
        'difference_x_range_min': 6,
        'difference_x_range_max': 6,
        'odds_1_min': 6,
        'odds_1_max': 6,
        'odds_1_min_second': 6,
        'odds_1_max_second': 6,
    }


    fieldsets = (
        {
            'title': 'Time frame',
            'icon': '',
            'icon_color': '',
            'fields': ('date_offset')
        },
        {
            'title': 'Odds settings',
            'icon': '',
            'icon_color': '',
            'fields': ('difference_x_range_min', 'difference_x_range_max', 'odds_1_min', 'odds_1_max',
                       'odds_1_min_second', 'odds_1_max_second')
         }
    )

    class Meta:
        model = DataFetchSettings
        exclude = ('user',)