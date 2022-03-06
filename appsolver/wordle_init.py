from django.core.files import File
import json, copy
from .wordle_solve import WordKnowledge, WORDLEN, PuzzleBoard, GUESSLEN, OneLetterGuess

# word list - load in from json file
# returns valid_words list
def readinwords():    
    f = open('/home/jacox/code/wsolver/appsolver/static/appsolver/wordledictionary.json')
    # alt - f = open('bigdictionary.json')
    myfile = File(f)
    wordList = json.load(myfile)
    myfile.close
    f.close

    # initialize valid_words lists - dictionary with words of proper length
    # and with T or F indicating whether word valid with current Knowledge
    all_words = []
    for word in wordList:
        if len(word) == WORDLEN and word.isalpha():
            all_words.append(word)
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