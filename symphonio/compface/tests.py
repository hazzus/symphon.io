from django.test import TestCase
from PIL import Image
from .models import Composer, add_composer_encoding
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


def count_matches(images_dir, composer):
    print('Counting', images_dir, composer.name)
    images = os.listdir(images_dir)
    count = len(images)
    success = 0
    for image in images:
        result = recognize_image(Image.open(open(os.path.join(images_dir, image), 'rb')))
        if result == [composer.id]:
            success += 1
        else:
            print(image, 'not recognized')
    return count, success


class StatisticTestCase(TestCase):
    images_dir = os.path.join('compface', 'img')

    def setUp(self):
        # Learning one photo
        Composer.objects.create(first_name="Petr", name="Tchaikovsky One", bio="norm",
                                photo=ImageFile(open(os.path.join(self.images_dir, "dicaprio.jpg"), "rb")))

        # Learning all photos
        t_dir = os.path.join(self.images_dir, 'tchaik')
        t_listdir = os.listdir(t_dir)
        c = Composer.objects.create(first_name="Petr", name="Tchaikovsky All", bio="norm",
                                photo=ImageFile(open(os.path.join(t_dir, t_listdir[0]), "rb")))
        for image in t_listdir[1:]:
            add_composer_encoding(c.id, Image.open(open(os.path.join(t_dir, image), 'rb')))

    def test_tchaik_clear_one_stat(self):
        composer = Composer.objects.get(name="Tchaikovsky One")
        t_clear_dir = os.path.join(self.images_dir, 'tchaik')

        count, success = count_matches(t_clear_dir, composer)

        print('Efficiency:', success / count)
        self.assertEqual(success, count)
            
    def test_tchaik_clear_many_stat(self):
        composer = Composer.objects.get(name="Tchaikovsky All")
        t_clear_dir = os.path.join(self.images_dir, 'tchaik')

        count, success = count_matches(t_clear_dir, composer)

        print('Efficiency:', success / count)
        self.assertEqual(success, count)
	
