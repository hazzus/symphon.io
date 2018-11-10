from datetime import datetime

from django.http import HttpRequest, HttpResponseRedirect, HttpResponseNotFound
from django.shortcuts import render
from .forms import PhotoForm

from PIL import Image

from .recognize import recognize_image, recognize_url_image
from .models import Concert, Composer, Composition


def index(request):
    photo_form = PhotoForm()
    return render(request, 'index.html', {'form': photo_form})


def recognize(request: HttpRequest):
    if request.method != "POST":
        pass  # TODO: error
        raise NotImplementedError("non-post")
    photo_form = PhotoForm(request.POST, request.FILES)
    result_set = None
    if not photo_form.is_valid():
        pass  # TODO: error
        raise NotImplementedError("non-valid")
    if 'photo' in request.FILES:
        image_field = photo_form.cleaned_data['photo']
        image: Image.Image = Image.open(image_field)
        result_set = recognize_image(image)
    elif 'data' in photo_form.cleaned_data:
        result_set = recognize_url_image(photo_form.cleaned_data['data'])

    if not result_set:
        return render(request, 'failure.html', {'no': True})
    elif len(result_set) > 1:
        # TODO maybe choose one composer?
        return render(request, 'failure.html')
    else:
        assert len(result_set) == 1
        composer_id = result_set[0]
        # TODO: maybe check that composer_id exists in the database
        return HttpResponseRedirect('composer/%s' % composer_id)

def composer(request: HttpRequest, composer_id: int):
    try:
        comp = Composer.objects.get(pk=composer_id)
    except Composer.DoesNotExist:
        return HttpResponseNotFound()
    compositions = Composition.objects.filter(author=comp)
    return render(request, 'composer.html',
                  {'name': comp.name,
                   'biography': comp.bio,
                   'photo': comp.photo,
                   'compositions': compositions})


def affiche(request: HttpRequest, composer_id):
    concerts = Concert.objects.filter(composer=composer_id)
    return render(request, 'affiche.html', {'concerts': concerts})

def composers(request):
    comps = Composer.objects.all()
    return render(request, 'list_composers.html', {'composers': comps})