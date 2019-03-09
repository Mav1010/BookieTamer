from django import forms
from .models import DataFetchSettings


class DataFetchSettingsForm(forms.ModelForm):
    class Meta:
        model = DataFetchSettings
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(DataFetchSettingsForm, self).__init__(*args, **kwargs)
        self.label_suffix = ''
        self.fields['user'].widget = forms.HiddenInput()
        self.fields['user'].label = ''
