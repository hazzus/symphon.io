from django.test import TestCase
from PIL import Image
from .models import Composer
# from .trainer import add_composer_encoding
from .recognize import recognize_image
from django.core.files.images import ImageFile
import os

class FirstRecognitionTestCase(TestCase):

    def test_the_same_recognize(self):
        composer = Composer.objects.create(name="lol kekov", bio="norm",
                                           photo=ImageFile(open("compface/img/dicaprio.jpg", "rb")))
        # composer.save()
        image = Image.open(open("compface/img/dicaprio.jpg", "rb"))
        result = recognize_image(image)
        self.assertEqual(result, [composer.id])


class SecondRecognitionTestCase(TestCase):
    def test_no_match(self):
        composer = Composer.objects.create(name="lol kekov", bio="norm",
                                           photo=ImageFile(open("compface/img/dicaprio.jpg", "rb")))
        composer.save()
        image2 = Image.open(open("compface/img/tch.jpg", "rb"))
        result = recognize_image(image2)
        self.assertEqual(result, [-1])
        composer.delete()


class ThirdRecognitionTestCase(TestCase):
    def test_different_recognize(self):
        composer = Composer.objects.create(name="lol kekov", bio="norm",
                                           photo=ImageFile(open("compface/img/tchaik.png", "rb")))
        composer.save()
        image2 = Image.open(open("compface/img/tchaik.png", "rb"))
        result = recognize_image(image2)
        self.assertEqual(result, [composer.id])
        composer.delete()


class FourthRecognitionTestCase(TestCase):
    def test_nobody(self):
        composer = Composer.objects.create(name="lol kekov", bio="norm",
                                           photo=ImageFile(open("compface/img/dicaprio.jpg", "rb")))
        composer.save()
        image = Image.open(open("compface/img/forest.jpg", "rb"))
        result = recognize_image(image)
        self.assertEqual(result, [])
        composer.delete()

class StatisticTestCase(TestCase):
    def setUp(self):
        Composer.objects.create(first_name="lol", name="kekov", bio="norm",
                                           photo=ImageFile(open("compface/img/tch.jpg", "rb")))

    def test_tchaik_clear_stat(self):
        composer = Composer.objects.get(name="kekov") 
        image_dir = os.path.join('compface', 'img', 'tchaik')
        count = len(os.listdir(image_dir))
        success = 0
        for image in os.listdir(image_dir):
            result = recognize_image(Image.open(open(os.path.join(image_dir, image), 'rb')))
            if result == [composer.id]:
                success += 1
            else:
                print(image, 'not recognized')
        print('Efficiency:', success / count)
        self.assertEqual(success, count)
            
            
	
