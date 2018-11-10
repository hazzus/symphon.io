from django import forms

class PhotoForm(forms.Form):
    data = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs= {'style': 'display: none;', 'value': ''}
        )
    )
    photo = forms.ImageField(
        required=False,
        widget=forms.FileInput(
            attrs={'class': 'form-control', 'style': 'display: none;'}
        )
    )