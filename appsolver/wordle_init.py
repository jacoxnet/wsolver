from django.contrib.auth.models import User
import copy
from appsolver.wordle_solve import WordKnowledge, PuzzleBoard, OneLetterGuess
from appsolver.models import BigDWord, WordleWord

# Global Defaults
WORDLEN = 5
GUESSLEN = 6
DICT = 'td'

# word list - load in from json file
# returns valid_words list

def register_new_user(request):
    newusername = 'user' + str(User.objects.all().count())
    user = User.objects.create_user(newusername)
    user.save()
    request.session['user'] = user
    clear_board_data(request)
    return newusername

def clear_board_data(request):
    request.session['all_words'] = readinwords(request)
    request.session['valid_words'] = copy.deepcopy(request.session.get('all_words'))
    request.session['knowledge'] = initKnowledge(request.session.get('wordlen'))
    request.session['theboard'] = inittheboard(request)


def retrieve_settings(request):
    wordlen = int(request.session.get('wordlen', WORDLEN))
    if wordlen < 5 or wordlen > 12:
        wordlen = WORDLEN
    guesslen = int(request.session.get('guesslen', GUESSLEN))
    if guesslen < 4 or guesslen > 10:
        guesslen = GUESSLEN
    dict = request.session.get('dict', DICT)
    if dict != 'td' and dict != 'dd':
        dict = DICT
    request.session.flush()
    request.session['wordlen'] = wordlen
    request.session['guesslen'] = guesslen
    request.session['dict'] = dict
    return wordlen, guesslen, dict

def readinwords(request):
    if request.session.get('dict') == 'td':
        # times dic
        all_words = [word.word_text.upper() for word in WordleWord.objects.all()]
    else:
        # big dict - must filter for alpha and length
        all_words = [word.word_text.upper() for word in BigDWord.objects.filter(word_length=request.session.get('wordlen'), word_alpha=True)]
    return all_words

# initialize knowledge and return
def initKnowledge(wordlen):
    return WordKnowledge(wordlen)

# initialize the board
def inittheboard(request):
    wordlen = request.session.get('wordlen')
    guesslen = request.session.get('guesslen')
    tb = PuzzleBoard(wordlen, guesslen)

    for i in range(request.session.get('guesslen')):
        tb.board.append([])
        for j in range(request.session.get('wordlen')):
            tb.board[i].append(OneLetterGuess(' ', 'W', i * request.session.get('wordlen') + j))
    return tb
