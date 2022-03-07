from django.core.files import File
import json, copy
from .models import WordleWord, BigDWord

def readinwords():    
    # f = open('/home/jacox/code/wsolver/appsolver/static/appsolver/wordledictionary.json')
    f = open('/home/jacox/code/wsolver/appsolver/static/appsolver/bigdictionary.json')
    myfile = File(f)
    wordList = json.load(myfile)
    myfile.close
    f.close
    
    w_list = []
    for word in wordList:
        wd = BigDWord(word_text=word)
        w_list.append(wd)
        
    
    BigDWord.objects.bulk_create(w_list)
