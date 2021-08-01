from django import forms
from django.forms import widgets


class DateInput(forms.DateInput):
        input_type = 'datetime-local'

class ModelForm(forms.Form):
        from_date = forms.DateField(widget=DateInput(attrs={'class': 'date'}), required=False)
        to_date = forms.DateField(widget=DateInput(attrs={'class': 'date'}), required=False )
