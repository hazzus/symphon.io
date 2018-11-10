from django.contrib import admin

from .models import Composer, Composition, Concert, ComposerRecognitionData

admin.site.register(Composer)
admin.site.register(Composition)
admin.site.register(Concert)
admin.site.register(ComposerRecognitionData)
