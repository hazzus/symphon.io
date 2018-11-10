from django.shortcuts import render
from compface.forms import PhotoForm
from PIL import Image
from compface.models import add_composer_encoding
from django.http import HttpResponseRedirect


def admin_page(request):
    return render(request, 'admin_page.html')


def add_composer_photo(request):
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
        result_set = add_composer_encoding(request.POST.get("id", ""), image)

    if not result_set:
        return render(request, 'failure.html')
    elif len(result_set) > 1:
        raise NotImplementedError("recognized too much")
    else:
        assert len(result_set) == 1
        composer_id = result_set[0]
        # TODO: maybe check that composer_id exists in the database
        return HttpResponseRedirect('composer/%s' % composer_id)
