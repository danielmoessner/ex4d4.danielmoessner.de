from django import forms


class GelbeSeitenForm(forms.Form):
    category = forms.CharField()
    location = forms.CharField()

    def clean(self):
        location = self.cleaned_data['location']
        location = location.replace('ä', 'ae').replace('ö', 'oe').replace('ü', 'ue').replace('ß', 'ss')
        location = location.lower()
        self.cleaned_data['location'] = location
        category = self.cleaned_data['category']
        category = category.replace('ä', 'ae').replace('ö', 'oe').replace('ü', 'ue').replace('ß', 'ss')
        category = category.lower()
        self.cleaned_data['category'] = category
