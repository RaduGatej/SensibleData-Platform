from django.db import models
from django.contrib.auth.models import User


class Participant(models.Model):
    user = models.OneToOneField(User)
    pseudonym = models.CharField(max_length=100, blank=True)

class Extra(models.Model):
    user = models.OneToOneField(User)
    phone = models.CharField(max_length=100, blank=True)
