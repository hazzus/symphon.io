from django import forms

class PhotoForm(forms.Form):
    data = forms.CharField(
        widget=forms.TextInput(
            attrs= {'style': 'display: none;'}
        )
    )
    photo = forms.ImageField(
        required=False,
        widget=forms.FileInput(
            attrs={'class': 'form-control', 'style': 'display: none;'}
        )
    )