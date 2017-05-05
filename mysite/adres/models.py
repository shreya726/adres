from django.db import models


class Word(models.Model):
    primary_word = models.CharField(max_length=20)
    related_word = models.CharField(max_length=20)
