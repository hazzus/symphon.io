from django.db import models
from django.utils import timezone

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
