from django.core.files import File
import json, copy
from .wordle_solve import WordKnowledge, WORDLEN, PuzzleBoard, GUESSLEN, DICT, OneLetterGuess
from .models import BigDWord, WordleWord, ValidWord

# word list - load in from json file
# returns valid_words list

def readinwords(request):
    try:
        # is there already session default settings
        dict = request.session.get('dict')
    except:
        # no - set them up
        request.session['wordlen'] = WORDLEN
        request.session['guesslen'] = GUESSLEN
        request.session['dict'] = DICT
    if request.session.get('dict') == 'td':
        # times dic
        all_words = [word.word_text.upper() for word in WordleWord.objects.all()]
    else:
        # big dict - must filter for alpha and length
        all_words = [word.word_text.upper() for word in BigDWord.objects.filter(word_length=request.session.get('wordlen'), word_alpha=True)]
    return all_words

# initialize knowledge and return
def initKnowledge():
    return WordKnowledge()

# initialize the board
def inittheboard(request):
    tb = PuzzleBoard()

    for i in range(request.session.get('guesslen')):
        tb.board.append([])
        for j in range(request.session.get('wordlen')):
            tb.board[i].append(OneLetterGuess(' ', 'W', i * request.session.get('wordlen') + j))
    return tb
