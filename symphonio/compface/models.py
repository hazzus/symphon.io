from django.db import models
from django.dispatch import receiver
from django.utils import timezone
from django.core.validators import MaxValueValidator, MinValueValidator
import numpy
import pickle
import face_recognition

from PIL import Image


class Composer(models.Model):
    class Meta:
        verbose_name = 'Композитор'
        verbose_name_plural = 'Композиторы'

    name = models.CharField(max_length=255, verbose_name='Фамилия')
    first_name = models.CharField(max_length=255, default='', verbose_name='Имя')
    patronymic = models.CharField(max_length=255, default='', blank=True, verbose_name='Отчество')
    bio = models.TextField(default="", verbose_name='Краткая биография')
    photo = models.ImageField(verbose_name='Портрет')
    creation_time = models.DateTimeField(default=timezone.now, verbose_name='Время создания')

    def __str__(self):
        return 'Композитор: %s' % self.name

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

    author = models.ForeignKey(Composer, on_delete=models.CASCADE, verbose_name='Композитор')
    name = models.CharField(max_length=255, verbose_name='Название')
    source = models.FileField(verbose_name='Файл')

    def __str__(self):
        return self.author.name + ' - ' + self.name


class Concert(models.Model):
    class Meta:
        verbose_name = 'Концерт'
        verbose_name_plural = 'Концерты'

    composer = models.ForeignKey(Composer, on_delete=models.CASCADE, verbose_name='Композитор')
    creation_time = models.DateTimeField(default=timezone.now, verbose_name='Время создания')
    start_time = models.DateTimeField(verbose_name='Время начала концерта')
    place = models.CharField(max_length=255, verbose_name='Место проведения концерта')
    url = models.URLField(max_length=255, default='', verbose_name='Ссылка на анонс')
    description = models.TextField(verbose_name='Краткое описание')

    def __str__(self):
        return 'Concert: of %s at %s, as described: %s' % (
            self.composer, self.place, self.description)


class ComposerRecognitionData(models.Model):
    composer = models.ForeignKey(Composer, on_delete=models.CASCADE, verbose_name='Композитор')
    data = models.BinaryField(verbose_name='Данные')


class Compilation(models.Model):
    class Meta:
        verbose_name = 'Подборка'
        verbose_name_plural = 'Подборки'

    name = models.CharField(max_length=255, verbose_name='Название')
    photo = models.ImageField( verbose_name='Изображение для подборки')
    description = models.TextField(default="авторская подборка", verbose_name='Описание подборки')
    compositions = models.ManyToManyField(Composition, verbose_name='Композиции')
    medium_age = models.IntegerField(
        default=35,
        validators= [
            MaxValueValidator(100),
            MinValueValidator(1)
        ], verbose_name='Средний возраст слушателя'
    )

    def __str__(self):
        return 'Подборка {}'.format(self.name)


class User(models.Model):
    MALE = 'M'
    FEMALE = 'F'
    GENDER_CHOICES = ((MALE, 'Male'), (FEMALE, 'Female'))
    creation_time = models.DateTimeField(default=timezone.now, verbose_name='Время создания')
    name = models.CharField(max_length=255, verbose_name='Имя')
    email = models.EmailField(verbose_name='E-mail')
    age = models.IntegerField(verbose_name='Возраст')
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, verbose_name='Пол')


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
