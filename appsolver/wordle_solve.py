import copy
import random
import multiprocessing as mp
import time

from appsolver.listofwords import ALLWORDS, SOLUTIONS

THREADS = 5
WORDLEN = 5
GUESSLEN = 6

# LetterGuess contains a representation of a single letter of a guess. It has both
# letter and color attributes. A guess is a list of LetterGuesses. A Puzzleboard is a 
# list of guesses.
# Letters are capital letters. Guesses are B(lack), Y(ellow), G(reen), W(hite). cid is the
# id of the square (guess * WORDLEN + cell across)

# theboard is composed of list of guesses
class OneLetterGuess:
        
    def __init__(self, l, c, i):
        self.letter = l
        self.color = c
        self.cid = i
    
class PuzzleBoard:

    def __init__(self, wordlen, guesslen):
        self.wordlen = wordlen
        self.guesslen = guesslen
        self.board = []
        self.current_guess = 0




# contains what we know about each letter position (e.g., 0-4)
# There is a PositionList instance for each position
# code:  '+' letter confirmed in that position
#        '-' letter confirmed NOT in that position
#        '^' letter possible in that position but not confirmed

class PositionList:
    def __init__(self):
        self.letter = {}
        # set all positions and letters to ^ (possible not confirmed)
        for i in range(ord('A'), ord('Z') + 1):
            self.letter[chr(i)] = '^'

class WordKnowledge:

    # structure for scoring guess words
    guessWords = SOLUTIONS + ALLWORDS

    def __init__(self, wordlen, all_words, valid_words):
        self.wordlen = wordlen
        self.all_words = all_words
        self.valid_words = valid_words
        self.position = []
        for i in range(self.wordlen):
            self.position.append(PositionList())
        # mandatory letters but not in a specific position
        self.mandatory = []
    
    
    def addman(self, ltr):
        if ltr not in self.mandatory:
            self.mandatory.append(ltr)

    def removeman(self, ltr):
        if ltr in self.mandatory:
            self.mandatory.remove(ltr)
    
    def isman(self, ltr):
        return (ltr in self.mandatory)
        
    # confirm a letter in a specific position
    def confirm(self, posn, ltr):
        for i in range(ord('A'), ord('Z') + 1):
            self.position[posn].letter[chr(i)] = '-'
        self.position[posn].letter[ltr] = '+'

    # rule out a letter in a specific position
    def rule_out(self, posn, ltr):
        self.position[posn].letter[ltr] = '-'
    
    # rule out a letter in all positions
    # except if already specific position (G)
    # or already on mandatory list (Y)
    # to account for double letter situation
    def rule_out_all(self, posn, ltr):
        # if already in mandatory, only rule out here
        if ltr in self.mandatory:
            self.position[posn].letter[ltr] = '-'
        # otherwise, rule out everywhere not already declared a G
        else:
            for i in range(self.wordlen):
                if self.position[i].letter[ltr] != '+':
                    self.position[i].letter[ltr] = '-'

    def test_word(self, word):
        # test a word to see if comports with knowledge. Returns T or F
        for i in range(len(word)):
            if self.position[i].letter[word[i]] == '-':
                return False
        for j in range(0, len(self.mandatory)):
            if self.mandatory[j] not in word:
                return False
        return True

    # go through list of words passed (valid_words) and
    # test to see if they meet current knowledge criteria
    # returns updated word list
    def updateValidWordList(self):
        for word in copy.copy(self.valid_words):
            if not self.test_word(word):
                self.valid_words.remove(word)

    # update knowledge based on color response to guess word
    # response is in the form of a string of G, B, and Y. 
    #   G - green (letter correct in proper position)
    #   Y - yellow (letter correc in wrong position)
    #   B - black or shadow (letter not in word)
    def update_knowledge(self, guess, response):
        for i in range(len(response)):
            if response[i] == 'G':
                # confirm where required 
                self.confirm(i, guess[i])
            if response[i] == 'Y':
                # rule out here and add to mandatory list
                self.rule_out(i, guess[i])
                self.addman(guess[i])
            if response[i] == 'B':
                # rule out everywhere unless G somewhere else
                self.rule_out_all(i, guess[i])

    # take guess and secret word and calculate a color response
    #   G - green (letter correct in proper position)
    #   Y - yellow (letter correc in wrong position)
    #   B - black or shadow (letter not in word)
    # because there can be duplicate letters, when we find a match we
    # replace the letter in the secret with space so it isn't found again
    @staticmethod
    def colorCalc(guess, secret):
        listSecret = list(secret)
        response = WORDLEN * [' ']
        for i in range(len(guess)):
            if guess[i] == listSecret[i]:
                response[i] = 'G'
                listSecret[i] = ' '
        for i in range(len(guess)):
            if response[i] != 'G' and guess[i] in listSecret:
                response[i] = 'Y'
                listSecret[listSecret.index(guess[i])] = ' '
        response = [item if item != ' ' else 'B' for item in response]
        return ''.join(response)

    # given a guessword, returns the expected size of resulting groupings
    # that guess word could divide the solution words
    def scoreGuess(self, guessWord):
        rdict = {}
        for testword in self.valid_words:
            result = WordKnowledge.colorCalc(guessWord, testword)
            if result in rdict:
                rdict[result] = rdict[result] + 1
            else:
                rdict[result] = 1
        s = sum([v ** 2 for v in rdict.values()]) / sum(rdict.values())
        #print(f"Scoring {guessWord}, {s} {rdict}")
        return s


    def allMins(self, wordList, scoreList):
        # find minimum value
        mm = min(scoreList)
        #create list of all minimum words
        rv = [word for word in wordList if scoreList[wordList.index(word)] == mm]
        print (f"Len rv is {len(rv)}")
        # create smaller list of secretwords in earlier list
        sv = [secretWord for secretWord in rv if secretWord in self.valid_words]
        print (f"Len sv is {len(sv)}")
        # return only secret words if there are some
        if len(sv) > 0:
            return sv
        else:
            return rv              

    # figure out word marked active with largest score and return
    def nextGuess(self):
        print('Evaluating ', len(self.valid_words), 'possibilities')
        if len(self.valid_words) == 1:
            return self.valid_words
        start = time.time()
        p = mp.Pool(processes=THREADS)
        guessWordsResults = list(p.map(self.scoreGuess, self.all_words))
        endtime = time.time()
        print(f'Threads {THREADS} total time: {endtime - start}')
        s = self.allMins(list(self.all_words), guessWordsResults)
        print(s)
        return s
