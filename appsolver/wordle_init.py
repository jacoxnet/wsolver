from django.core.files import File
import json, copy
from .wordle_solve import WordKnowledge, WORDLEN, PuzzleBoard, GUESSLEN, OneLetterGuess
from .models import BigDWord, WordleWord, ValidWord

# word list - load in from json file
# returns valid_words list
def readinwords():    
    all_words = [word.word_text for word in WordleWord.objects.all()]
    return all_words

# initialize knowledge and return
def initKnowledge():
    return WordKnowledge()

# initialize the board
def inittheboard():
    tb = PuzzleBoard()

    for i in range(GUESSLEN):
        tb.board.append([])
        for j in range(WORDLEN):
            tb.board[i].append(OneLetterGuess(' ', 'W', i * WORDLEN + j))
    return tb
