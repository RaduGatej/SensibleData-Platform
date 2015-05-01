from django.db import models
from django.contrib.auth.models import User


class Participant(models.Model):
    user = models.OneToOneField(User)
    pseudonym = models.CharField(max_length=100, blank=True)
    cpr = models.CharField(max_length=100, unique=True)


class Extra(models.Model):
    user = models.OneToOneField(User)
    phone = models.CharField(max_length=100, blank=True)


class Child(models.Model):
    user = models.ForeignKey(User)
    cpr = models.CharField(max_length=20)
    name = models.CharField(max_length=100)
    questionnaire_id = models.CharField(max_length=100)

