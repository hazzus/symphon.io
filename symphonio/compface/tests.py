from django.test import TestCase
import symphonio.compface.recognize as recognize


class FaceRecognitionTestCase(TestCase):

    def test_DiCaprio_is_recognized(self):
        result = recognize.recognize("dicaprio2")
        self.assertEqual(result, True)
