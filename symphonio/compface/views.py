from django.shortcuts import render
from .forms import PhotoForm
# Create your views here.

def index(request):
    if request.method == 'GET':
        photo_form = PhotoForm()
        return render(request, "index.html", {'form': photo_form})
    else:
        pass
