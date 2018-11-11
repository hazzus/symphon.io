from django.db import models
from django.dispatch import receiver
from django.utils import timezone
import numpy
import pickle
import face_recognition

from PIL import Image


class Composer(models.Model):
    class Meta:
        verbose_name = 'Композитор'
        verbose_name_plural = 'Композиторы'

    name = models.CharField(max_length=255)
    first_name = models.CharField(max_length=255, default='')
    patronymic = models.CharField(max_length=255, default='', blank=True)
    bio = models.TextField(default="")
    photo = models.ImageField()
    creation_time = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return 'Composer: %s' % self.name

    def save(self, *args, **kwargs):
        super(Composer, self).save(*args, **kwargs)
        image = Image.open(self.photo)
        (width, height) = image.size
        if width < height:
            image = image.resize((300, height * 300 // width))
        else:
            image = image.resize((width * 300 // height, 300))
        if width == 300:
            image = image.crop((0, 0, 300, 300))
        else:
            image = image.crop((0, 0, 300, 300))
        image.save(self.photo.path)


class Composition(models.Model):
    class Meta:
        verbose_name = 'Композиция'
        verbose_name_plural = 'Композиции'

    author = models.ForeignKey(Composer, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    source = models.FileField()

    def __str__(self):
        return self.author.name + ' - ' + self.name


class Concert(models.Model):
    class Meta:
        verbose_name = 'Концерт'
        verbose_name_plural = 'Концерты'

    composer = models.ForeignKey(Composer, on_delete=models.CASCADE)
    creation_time = models.DateTimeField(default=timezone.now)
    start_time = models.DateTimeField('start of the concert')
    place = models.CharField(max_length=255)
    url = models.URLField(max_length=255, default='')
    description = models.TextField()

    def __str__(self):
        return 'Concert: of %s at %s, as described: %s' % (
            self.composer, self.place, self.description)


class ComposerRecognitionData(models.Model):
    composer = models.ForeignKey(Composer, on_delete=models.CASCADE)
    data = models.BinaryField()


class Compilation(models.Model):
    class Meta:
        verbose_name = 'Подборка'
        verbose_name_plural = 'Подборки'

    name = models.CharField(max_length=255)
    photo = models.ImageField()
    description = models.TextField(default="авторская подборка")
    compositions = models.ManyToManyField(Composition)



class User(models.Model):
    MALE = 'M'
    FEMALE = 'F'
    GENDER_CHOICES = ((MALE, 'Male'), (FEMALE, 'Female'))
    creation_time = models.DateTimeField(default=timezone.now)
    name = models.CharField(max_length=255)
    email = models.EmailField()
    age = models.IntegerField()
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)


def get_photo_encoding(image):
    return face_recognition.face_encodings(numpy.array(image))[0]


def add_composer_encoding(id, image):
    image = image.convert('RGB')
    try:
        encoding = get_photo_encoding(image)
    except IndexError:
        return False
    composer = Composer.objects.get(pk=id)
    composer_encoded = ComposerRecognitionData.objects.create(
        composer=composer, data=pickle.dumps(encoding))
    composer_encoded.save()
    return True


@receiver(models.signals.post_save, sender=Composer)
def establish_encoding_after_save(sender, instance, **kwargs):
    image = Image.open(instance.photo.open("rb"))
    add_composer_encoding(instance.id, image)
