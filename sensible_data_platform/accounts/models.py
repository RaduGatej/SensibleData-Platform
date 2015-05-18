from django.db import models
from django.contrib.auth.models import User


class CPRNumber(models.Model):
    cpr = models.CharField(max_length=255)


class Participant(models.Model):
    user = models.OneToOneField(User)
    pseudonym = models.CharField(max_length=100, blank=True)
    cpr = models.OneToOneField(CPRNumber)


class Extra(models.Model):
    user = models.OneToOneField(User)
    phone = models.CharField(max_length=100, blank=True)


class Child(models.Model):
    user = models.ForeignKey(User)
    cpr = models.OneToOneField(CPRNumber)
    name = models.CharField(max_length=100)
    questionnaire_id = models.CharField(max_length=100)
    relation_to_user = models.CharField(max_length=100, null=True)
    email = models.CharField(max_length=100, null=True)
    notified = models.BooleanField()

