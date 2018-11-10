from django.shortcuts import render

from .forms import AddPhotoToComposerForm

from PIL import Image
from compface.models import add_composer_encoding
from django.http import HttpResponseRedirect, HttpResponseForbidden


def admin_page(request):
    if not request.user.is_superuser:
        return HttpResponseForbidden()
    form = AddPhotoToComposerForm()
    return render(request, 'admin_page.html', {'form': form})


def add_composer_photo(request):
    if request.method != "POST":
        pass  # TODO: error
        raise NotImplementedError("non-post")
    photo_form = AddPhotoToComposerForm(request.POST, request.FILES)
    if not photo_form.is_valid():
        pass  # TODO: error
        raise NotImplementedError("non-valid")
    if 'photo' in request.FILES:
        image_field = photo_form.cleaned_data['photo']
        image: Image.Image = Image.open(image_field)
        result = add_composer_encoding(photo_form.cleaned_data.get('composer').pk, image)
        if result:
            return render(request, 'admin_page.html', {'success': True, 'form': AddPhotoToComposerForm()})
        else:
            return render(request, 'admin_page.html', {'danger': True, 'form': AddPhotoToComposerForm()})
