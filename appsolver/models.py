from django.db import models

# Create your models here.

class MyDictionary(models.Model):
    word_text = models.CharField(max_length=50)
    