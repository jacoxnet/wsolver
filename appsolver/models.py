from django.db import models

# Create your models here.

class Word(models.Model):
    word_text = models.CharField(max_length=50)
    word_source = models.CharField(max_length=50)
    