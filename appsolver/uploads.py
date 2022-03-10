from django.core.files import File
import json, copy
from .models import WordleWord, BigDWord

def readinwords():    
    
    wordList = BigDWord.objects.all()
    for word in wordList:
        word.word_length = len(word.word_text)
        word_alpha = word.isalpha()
        word.save()
