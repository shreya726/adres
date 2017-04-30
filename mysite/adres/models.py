from django.db import models

# Create your models here.
class Word(models.Model):
	word = models.CharField(max_length=20)
	
class Document(models.Model):
    docfile = models.FileField(upload_to='documents/%Y/%m/%d')