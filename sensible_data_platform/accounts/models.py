from django.db import models
from django.contrib.auth.models import User

class Cas(models.Model):
    user = models.OneToOneField(User)
    student_id = models.CharField(max_length=100, blank=True)
    email = models.CharField(max_length=100, blank=True)
    givenName = models.CharField(max_length=100, blank=True)
    familyName = models.CharField(max_length=100, blank=True)
    closed = models.CharField(max_length=100, blank=True)
