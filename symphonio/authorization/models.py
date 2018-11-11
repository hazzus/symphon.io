from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

MALE = 'M'
FEMALE = 'F'
NON_DISCLOSED = 'N'


class Profile(models.Model):
    GENDER_CHOICES = ((MALE, 'Male'), (FEMALE, 'Female'), (NON_DISCLOSED,
                                                           'Non disclosed'))
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    vk_id = models.CharField(max_length=50, unique=True, blank=True)
    age = models.IntegerField(null=True, blank=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True)

    def __str__(self):
        return self.user.username
