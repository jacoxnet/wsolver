from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render
from django.contrib import messages
from django.urls import reverse

import csv
from datetime import datetime

from .wordle_init import theboard, initall
from .wordle_solve import WORDLEN, OneLetterGuess

# Create your views here.

# route /
def index(request):
    if request.method == "GET":
        context = {
            "theboard": theboard.board
        }
        return render(request, "appsolver/index.html", context)
    elif request.method == "POST":
        guessword = request.POST["guessword"]
        if len(guessword) != WORDLEN:
            # also test if a valid guess word
            # if not return message and go back to 
            # return HttpResponseRedirect(reverse("guess"))
            messages.add_message(request, messages.INFO, "Invalid guess")
            return HttpResponseRedirect(reverse("index"))
        g = []
        print('adding', guessword, ' to board at position ', theboard.current_guess)
        for i in range(len(guessword)):
            letter = guessword[i]
            g.append(OneLetterGuess(letter.upper(), 'W', theboard.current_guess*WORDLEN + i))
        theboard.board[theboard.current_guess] = g

        context = {
            "theboard": theboard.board,
            "lowid": theboard.current_guess * WORDLEN,
            "highid": WORDLEN
        }
        theboard.current_guess = theboard.current_guess + 1
        return render(request, "appsolver/validate.html", context)

# route /guess
def guess(request):
    if request.method == "GET":
        context = {
            "theboard": theboard.board,
            "status": "validate_guess",
            "wordlen": WORDLEN
        }
        return render(request, "appsolver/index.html", context)    

# route settings/
def settings(request):
    context = {
        "wordlen": 5,
        "guesses": 6
    }
    return render(request, "appsolver/settings.html", context)

def clear(request):
    valid_words, knowledge, theboard = initall()
    messages.add_message(request, messages.INFO, "Board Cleared")
    return HttpResponseRedirect(reverse("index"))
