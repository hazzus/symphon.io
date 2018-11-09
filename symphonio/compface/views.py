from django.http import HttpRequest
from django.shortcuts import render
from .forms import PhotoForm
from .models import Composer, Composition

from PIL import Image

from .recognize import recognize_image


def index(request):
    photo_form = PhotoForm()
    return render(request, 'index.html', {'form': photo_form})


def recognize(request: HttpRequest):
    if request.method != "POST":
        pass  # TODO: error
        raise NotImplementedError("non-post")
    photo_form = PhotoForm(request.POST, request.FILES)
    if not photo_form.is_valid():
        pass  # TODO: error
        raise NotImplementedError("non-valid")
    if 'photo' in request.FILES:
        image_field = photo_form.cleaned_data['photo']
        image: Image.Image = Image.open(image_field)
        result_set = recognize_image(image)
        if not result_set:
            raise NotImplementedError("can't recognize anything")
        elif len(result_set) > 1:
            raise NotImplementedError("recognized too much")
        else:
            assert len(result_set) == 1
            composer_id = result_set[0]
            # TODO: maybe check that composer_id exists in the database
            return render(request, 'composers/%s' % composer_id)
    elif 'data' in photo_form.cleaned_data:
        recognize_image()
        # TODO from dara url to face recognition


def composer(request: HttpRequest, composer_id: int):
    comp = Composer.objects.get(pk=composer_id)
    compositions = Composition.objects.filter(author=comp)
    return render(request, 'composer.html',
                  {'name': comp.name,
                   'biography': comp.bio,
                   'photo': comp.photo,
                   'compositions': compositions})
