from django import forms
from .models import DataFetchSettings


class DataFetchSettingsForm(forms.Form):
    class Meta:
        model = DataFetchSettings

    # def __init__(self, *args, **kwargs):
    #     super(DataFetchSettingsForm, self).__init__(*args, **kwargs)
    #     self.fields['user'].initiall =