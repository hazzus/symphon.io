from django.test import TestCase
from PIL import Image
from .models import Composer, add_composer_encoding
# from .trainer import add_composer_encoding
from .recognize import recognize_image
from django.core.files.images import ImageFile
import os

images_dir = os.path.join('compface', 'img')


class BasicRecognitionTestCase(TestCase):
    tchaikovsky = os.path.join(images_dir, 'Tchaikovsky.jpg')
    another_tchaikovsky = os.path.join(images_dir, 'Tchaikovsky_2.jpg')
    rakhmaninov = os.path.join(images_dir, 'Rakhmaninov.jpg')
    forest = os.path.join(images_dir, 'forest.jpg')

    def setUp(self):
        self.composer = Composer.objects.create(name="Test1", bio="test",
                                                photo=ImageFile(open(self.tchaikovsky, "rb")))

    def test_the_same_recognize(self):
        image = Image.open(open(self.tchaikovsky, "rb"))
        result = recognize_image(image)
        self.assertEqual(result, [self.composer.id])

    def test_no_match(self):
        image = Image.open(open(self.rakhmaninov, "rb"))
        result = recognize_image(image)
        self.assertEqual(result, [-1])

    def test_different_recognize(self):
        image = Image.open(open(self.another_tchaikovsky, "rb"))
        result = recognize_image(image)
        self.assertEqual(result, [self.composer.id])

    def test_nobody(self):
        image = Image.open(open(self.forest, "rb"))
        result = recognize_image(image)
        self.assertEqual(result, [])


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


class StatisticOnePhotoTestCase(TestCase):

    def setUp(self):
        # Learning one photo
        Composer.objects.create(first_name="Petr", name="Tchaikovsky One", bio="norm",
                                photo=ImageFile(open(os.path.join(images_dir, "Tchaikovsky.jpg"), "rb")))

    def test_tchaik_clear_one_stat(self):
        composer = Composer.objects.get(name="Tchaikovsky One")
        t_clear_dir = os.path.join(images_dir, 'tchaik')

        count, success = count_matches(t_clear_dir, composer)

        print('Efficiency:', success / count)
        self.assertEqual(success, count)


class StatisticMultiplePhotoTestCase(TestCase):

    def setUp(self):
        # Learning all photos
        t_dir = os.path.join(images_dir, 'tchaik')
        t_listdir = os.listdir(t_dir)
        c = Composer.objects.create(first_name="Petr", name="Tchaikovsky All", bio="norm",
                                    photo=ImageFile(open(os.path.join(t_dir, t_listdir[0]), "rb")))
        for image in t_listdir[1:]:
            add_composer_encoding(c.id, Image.open(open(os.path.join(t_dir, image), 'rb')))

    def test_tchaik_clear_many_stat(self):
        composer = Composer.objects.get(name="Tchaikovsky All")
        t_clear_dir = os.path.join(images_dir, 'tchaik')

        count, success = count_matches(t_clear_dir, composer)

        print('Efficiency:', success / count)
        self.assertEqual(success, count)
