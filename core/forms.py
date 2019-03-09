from django import forms


""" default form styling using Boostrap classes """
class BootstrapStylingBaseForm(forms.Form):
    field_cols = None

    def __init__(self, *args, **kwargs):
        super(BootstrapStylingBaseForm, self).__init__(*args, **kwargs)
        field_index = 0

        while field_index <= len(self.fields):
            for field in self.fields:
                # used to define col-lg-xx Bootstrap class for each field
                if self.field_cols:
                    if field in self.field_cols:
                        self.fields[field].widget.attrs.update({'count_cols': self.field_cols.get(field)})
                else:
                    self.fields[field].widget.attrs.update({'count_cols': 12})
            field_index += 1
