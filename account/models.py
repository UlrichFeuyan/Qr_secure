from django.contrib.auth.models import AbstractUser
from django.db import models

SEXE_CHOICES = [
    ('masculin', 'Masculin'),
    ('feminin', 'Féminin'),
]


class CustomUser(AbstractUser):
    sex = models.CharField(max_length=15, choices=SEXE_CHOICES, null=True)
    phone = models.CharField(max_length=35, null=True)

    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=False)
