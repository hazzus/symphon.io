from django.contrib import admin
from django.contrib.auth.models import User, Group
from .models import Composer, Composition, Concert

admin.site.register(Composer)
admin.site.register(Composition)
admin.site.register(Concert)