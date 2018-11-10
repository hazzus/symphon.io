from django import forms
from compface.models import Composer

class AddPhotoToComposerForm(forms.Form):
    composer = forms.ModelChoiceField(
        queryset=Composer.objects.all(),
        widget=forms.Select(
            attrs={'class': 'form-control', 'placeholder': 'Выберите композитора'}
        )
    )
    photo = forms.ImageField(
        widget=forms.FileInput(
            attrs={'style': 'display: none;'}
        )
    )