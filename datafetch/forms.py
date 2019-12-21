from django import forms

from .models import DataFetchSettings
from core.forms import BootstrapStylingBaseForm


class DataFetchSettingsForm(BootstrapStylingBaseForm, forms.ModelForm):
    field_cols = {
        'date_offset': 2,
        'leagues': 4,
        'odds_1_min_probability': 2,
        'odds_1_max_probability': 2,
        'odds_2_min_probability': 2,
        'odds_2_max_probability': 2,
        'max_difference_x_probability': 2,
        'name': 12,
    }


    fieldsets = (
        {
            'title': 'Time frame and Leagues',
            'icon': '',
            'icon_color': '',
            'fields': ('date_offset', 'leagues')
        },
        {
            'title': 'Odds settings',
            'icon': '',
            'icon_color': '',
            'fields': ('odds_1_min_probability',
                       'odds_1_max_probability',
                       'odds_2_min_probability',
                       'odds_2_max_probability',
                       'max_difference_x_probability',
                       )
         },
        {
            'title': 'Name',
            'icon': '',
            'fields': ('name')
        }
    )

    class Meta:
        model = DataFetchSettings
        exclude = ('user',)

    def __init__(self, *args, **kwargs):
        super(DataFetchSettingsForm, self).__init__(*args, **kwargs)
        self.fields['leagues'].widget.attrs.update({'class': 'js-multiple-select2', 'style': 'width: 100%'})