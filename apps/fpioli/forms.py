from django import forms
from django.core.exceptions import ValidationError


class StartEndForm(forms.Form):
    first_number = forms.IntegerField()
    last_number = forms.IntegerField()

    def clean(self):
        first_number = self.cleaned_data['first_number']
        last_number = self.cleaned_data['last_number']
        if last_number < first_number:
            raise ValidationError('The last number needs to be greater than the first.')
