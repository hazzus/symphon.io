from django.db import models
from django.dispatch import receiver
from django.utils import timezone
from PIL import Image
from .recognize import known_faces, ids
import numpy
import pickle
import face_recognition

from PIL import Image

class Composer(models.Model):
    name = models.CharField(max_length=255)
    bio = models.TextField(default="")
    photo = models.ImageField(default='anton.png')
    creation_time = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return 'Composer: %s' % self.name

    def save(self, *args, **kwargs):
        super(Composer, self).save(*args, **kwargs)
        image = Image.open(self.photo)
        (width, height) = image.size
        image = image.resize((300, height * 300 // width))
        image.save(self.photo.path)

class Composition(models.Model):
    author = models.ForeignKey(Composer, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    source = models.FileField()

    def __str__(self):
        return self.author.name + ' - ' + self.name


class Concert(models.Model):
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


def get_photo_encoding(image):
    return face_recognition.face_encodings(numpy.array(image))


composers = ComposerRecognitionData.objects.all()
for composer in composers:
    known_faces.append(pickle.loads(composer.data))
    ids.append(composer.composer.id)


def add_composer_encoding(id, image):
    try:
        encoding = get_photo_encoding(image)
    except IndexError:
        print("Could not find any face")
        return
    composer = Composer.objects.get(pk=id)
    composer_encoded = ComposerRecognitionData.objects.create(composer=composer, data=pickle.dumps(encoding))
    composer_encoded.save()
    known_faces.append(face_recognition.face_encodings(numpy.array(image))[0])
    ids.append(id)


@receiver(models.signals.post_save, sender=Composer)
def establish_encoding_after_save(sender, instance, **kwargs):
    image = Image.open(instance.photo.open("rb"))
    add_composer_encoding(instance.id, image)
