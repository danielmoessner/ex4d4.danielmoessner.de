from django import forms


class PzmodeForm(forms.Form):
    name = forms.CharField()
    email = forms.CharField(required=False)
    phone = forms.CharField(required=False)
    message = forms.CharField(required=False)


class DynamicForm(forms.Form):
    pass
