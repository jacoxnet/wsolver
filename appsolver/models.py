from django.db import models

# Create your models here.

class BigDWord(models.Model):
    word_text = models.CharField(max_length=50)    

class WordleWord(models.Model):
    word_text = models.CharField(max_length=50)

class ValidWord(models.Model):
    word_text = models.CharField(max_length=50)
    score = models.SmallIntegerField(null=True)