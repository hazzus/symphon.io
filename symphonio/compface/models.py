from django.db import models
from django.utils import timezone
import pickle
import numpy
import face_recognition
from PIL import Image
from django.dispatch import receiver


def get_photo_encoding(image):
    image = numpy.array(image)
    return pickle.dumps(face_recognition.face_encodings(image)[0])


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
        image = image.resize((300, 300))
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


@receiver(models.signals.post_save, sender=Composer)
def establish_encoding_after_save(sender, instance, **kwargs):
    image = Image.open(instance.photo.open("rb"))
    recognition_data = ComposerRecognitionData.objects.create(composer=instance,
                                                              data=get_photo_encoding(image))
    recognition_data.save()
