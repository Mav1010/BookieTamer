from django import forms

from .models import DataFetchSettings
from core.forms import BootstrapStylingBaseForm


class DataFetchSettingsForm(BootstrapStylingBaseForm, forms.ModelForm):
    field_cols = {
        'date_offset': 4,
        'difference_x_range_min': 2,
        'difference_x_range_max': 2,
        'odds_1_min': 2,
        'odds_1_max': 2,
        'odds_1_min_second': 2,
        'odds_1_max_second':2,
    }


    fieldsets = (

    )

    class Meta:
        model = DataFetchSettings
        exclude = ('user',)