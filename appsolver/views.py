from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render
from django.contrib import messages
from django.urls import reverse

import csv
from datetime import datetime
import copy

from .wordle_init import readinwords, initKnowledge, inittheboard, retrieve_settings, register_new_user, clear_board_data
from .wordle_solve import WORDLEN, GUESSLEN, DICT, OneLetterGuess

# Create your views here.

# route /
def index(request):
    if request.method == "GET":
        # reset session data
        wordlen, guesslen, dict = retrieve_settings(request)
        print('board is ', wordlen, 'by ', guesslen, 'dict ', dict)
        username = register_new_user(request)
        print('your username is ', username)
        clear_board_data(request)
        return HttpResponseRedirect(reverse('guess'))
        
    elif request.method == "POST":
        theboard = request.session.get('theboard')
        guessword = request.POST["guessword"]
        if len(guessword) != WORDLEN:
            # also test if a valid guess word
            # if not return message and go back to 
            # return HttpResponseRedirect(reverse("guess"))
            messages.add_message(request, messages.INFO, "Invalid guess")
            return HttpResponseRedirect(reverse("guess"))
        guessword = guessword.upper()
        g = []
        print('adding', guessword, ' to board at position ', theboard.current_guess)
        for i in range(WORDLEN):
            theboard.board[theboard.current_guess][i].letter = guessword[i]
        request.session['last_guess'] = guessword
        context = {
            "theboard": theboard,
            "lowid": theboard.current_guess * WORDLEN,
            "highid": (theboard.current_guess + 1) * WORDLEN
        }
        request.session['theboard'] = theboard
        return render(request, "appsolver/validate.html", context)

def validate(request):
    if request.method == 'POST':
        theboard = request.session.get('theboard')
        validateguess = request.POST["validateguess"]
        print('got ', validateguess, ' from template')
        if len(validateguess) != WORDLEN or ' ' in validateguess:
            # space means a letter wasn't selected
            messages.add_message(request, messages.INFO, "Invalid response")
            return HttpResponseRedirect(reverse("validate"))
        # update the board
        for i in range(WORDLEN):
            theboard.board[theboard.current_guess][i].color = validateguess[i]
        theboard.current_guess = theboard.current_guess + 1
        last_guess = request.session.get('last_guess')
        k = request.session.get('knowledge')
        print('updating knowledge', last_guess, validateguess)
        k.update_knowledge(last_guess, validateguess)
        request.session['valid_words'] = k.getUpdatedWordList(request.session.get('valid_words'))
        request.session['theboard'] = theboard
        print('guess of ', validateguess, ' recorded')
        return HttpResponseRedirect(reverse("guess"))
        
    else:
        theboard = request.session.get('theboard')
        context = {
            "theboard": theboard,
            "lowid": theboard.current_guess * WORDLEN,
            "highid": (theboard.current_guess + 1) * WORDLEN
        }
        return render(request, "appsolver/validate.html", context)
            

# route /guess
def guess(request):
    if request.method == "GET":
        k = request.session.get('knowledge')            
        valid_words = request.session.get('valid_words')
        print('retrieved', len(valid_words), ' valid words')
        if len(valid_words) == 0:
            nowords = True
        else:
            nowords = False
        context = {
            "theboard": request.session.get('theboard'),
            "topwords": k.get_top_words(valid_words),
            "nowords": nowords
        }
        return render(request, "appsolver/index.html", context)    

# route clear
def clear(request):
    clear_board_data(request)
    messages.add_message(request, messages.INFO, "Board Cleared")
    return HttpResponseRedirect(reverse("index"))

# route settings/
def settings(request):
    if request.method == 'GET':
        context = {
            "wordlen": request.session.get('wordlen'),
            "guesses": request.session.get('guesslen'),
            "dict": request.session.get('dict')
        }
        return render(request, "appsolver/settings.html", context)
    else:
        request.session['wordlen'] = request.POST['wlen']
        request.session['guesslen'] = request.POST['glen']
        request.session['dict'] = request.POST['dictionary']

        messages.add_message(request, messages.INFO, f"New Settings Loaded: board size {request.session.get('wordlen')} by {request.session.get('guesslen')}")
    return HttpResponseRedirect(reverse("index"))

