from django import forms


class ShorterForm(forms.Form):
    full_link = forms.CharField(max_length=1000)
