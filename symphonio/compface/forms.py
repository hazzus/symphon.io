from django import forms

class PhotoForm(forms.Form):
    photo = forms.ImageField(
        widget=forms.FileInput(
            attrs={'class': 'form-control', 'style': 'display: none;'}
        )
    )