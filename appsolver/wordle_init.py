from django.contrib.auth.models import User
from appsolver.wordle_solve import WordKnowledge, PuzzleBoard, OneLetterGuess, WORDLEN, GUESSLEN, SOLUTIONS, ALLWORDS

# Global Defaults


def register_new_user(request):
    newusername = 'user' + str(User.objects.all().count())
    user = User.objects.create_user(newusername)
    user.save()
    request.session['user'] = user
    clear_board_data(request)
    return newusername

def clear_board_data(request):
    all_words = set([word.upper() for word in ALLWORDS + SOLUTIONS])
    valid_words = set([word.upper() for word in SOLUTIONS])    
    k = WordKnowledge(WORDLEN, all_words, valid_words)
    request.session['knowledge'] = k
    request.session['theboard'] = inittheboard(request)
    

# initialize the board
def inittheboard(request):
    tb = PuzzleBoard(WORDLEN, GUESSLEN)

    for i in range(GUESSLEN):
        tb.board.append([])
        for j in range(WORDLEN):
            tb.board[i].append(OneLetterGuess(' ', 'W', i * WORDLEN + j))
    return tb
