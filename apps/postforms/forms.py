from django import forms


class KostenvoranschlagForm(forms.Form):
    anrede = forms.ChoiceField(choices=(('Herr', 'Herr'), ('Frau', 'Frau')))
    vorname = forms.CharField()
    nachname = forms.CharField()
    email = forms.EmailField()
    telefon = forms.CharField()
    bild1 = forms.ImageField(required=True)
    bild2 = forms.ImageField(required=False)
    bild3 = forms.ImageField(required=False)
    bild4 = forms.ImageField(required=False)
    bild5 = forms.ImageField(required=False)
    bild6 = forms.ImageField(required=False)
