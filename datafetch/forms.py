from django import forms

from .models import DataFetchSettings


class DataFetchSettingsForm(forms.ModelForm):
    class Meta:
        model = DataFetchSettings
        exclude = ('user',)