from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class BigDWord(models.Model):
    word_text = models.CharField(max_length=50)
    word_length = models.SmallIntegerField(null=True)
    word_alpha = models.BooleanField(null=True)  

class WordleWord(models.Model):
    word_text = models.CharField(max_length=50)

class ValidWord(models.Model):
    word_text = models.CharField(max_length=50)
    score = models.SmallIntegerField(null=True)
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)