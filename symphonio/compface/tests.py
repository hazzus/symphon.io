from django.test import TestCase
from PIL import Image
from .models import Composer
from .trainer import add_composer_encoding
from .recognize import recognize_image
from django.core.files.images import ImageFile


class RecognitionTestCase(TestCase):

    def test_the_same_recognize(self):
        composer = Composer.objects.create(name="lol kekov", bio="norm",
                                           photo=ImageFile(open("compface/img/dicaprio.jpg", "rb")))
        composer.save()
        image = Image.open(open("compface/img/dicaprio.jpg", "rb"))
        result = recognize_image(image)
        self.assertEqual(result, [composer.id])

    def test_not_recognized(self):
        composer = Composer.objects.create(name="lol kekov", bio="norm",
                                           photo=ImageFile(open("compface/img/dicaprio.jpg", "rb")))
        composer.save()
        image2 = Image.open(open("compface/img/tch.jpg", "rb"))
        result = recognize_image(image2)
        self.assertEqual(result, [])

    def test_different_recognize(self):
        composer = Composer.objects.create(name="lol kekov", bio="norm",
                                           photo=ImageFile(open("compface/img/Чайковский_1.jpg", "rb")))
        composer.save()
        image2 = Image.open(open("compface/img/Чайковский_2.jpg", "rb"))
        result = recognize_image(image2)
        self.assertEqual(result, [composer.id])
