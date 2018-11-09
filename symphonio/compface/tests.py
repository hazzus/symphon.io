from django.test import TestCase
from PIL import Image
from .models import Composer
from .trainer import add_composer_encoding
from .recognize import recognize_image


class RecognitionTestCase(TestCase):

    def test_the_same_recognize(self):
        composer = Composer.objects.create(name="lol kekov")
        composer.save()
        image = Image.open(open("compface/img/dicaprio.jpg", "rb"))
        add_composer_encoding(composer.id, image)
        result = recognize_image(image)
        self.assertEqual(result, [composer.id])

    def test_not_recognized(self):
        composer = Composer.objects.create(name="lol kekov")
        composer.save()
        image = Image.open(open("compface/img/dicaprio.jpg", "rb"))
        image2 = Image.open(open("compface/img/tch.jpg", "rb"))
        add_composer_encoding(composer.id, image)
        result = recognize_image(image2)
        self.assertEqual(result, [])
