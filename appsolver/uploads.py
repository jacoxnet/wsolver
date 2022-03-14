from django.core.files import File
import json, copy
from appsolver.models import BigDWord, WordleWord

# first do big word list - load in from json file
# f = open('/home/jacox/code/words_dictionary.json')
# myfile = File(f)
# word_list = json.load(myfile)
# myfile.close
# f.close

# new_words = []
# for word in word_list:
#     new_words.append(BigDWord(word_text=word, word_length=len(word), word_alpha=word.isalpha()))

# n = BigDWord.objects.bulk_create(new_words)

# print('created', len(n), 'words')

# now do wordle list
f = open('/home/jacox/code/wordledictionary.json')
myfile = File(f)
word_list = json.load(myfile)
myfile.close
f.close

new_words = []
for word in word_list:
    new_words.append(WordleWord(word_text=word))

n = WordleWord.objects.bulk_create(new_words)

print('created', len(n), 'words')
