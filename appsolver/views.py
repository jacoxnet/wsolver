from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render
from django.contrib import messages
from django.urls import reverse

import csv
from datetime import datetime

from .wordle_init import readinwords, initKnowledge, inittheboard
from .wordle_solve import WORDLEN, GUESSLEN, OneLetterGuess

# Create your views here.

# route /
def index(request):
    if request.method == "GET":
        # is this user logged in?
        username = request.session.get('username', '0')
        if username == '0':
            print('I dont recognize you - registering as new')
            username = register_new_user(request)
        print('your username is ', username)
        context = {
            "theboard": request.session.get('theboard')
        }
        return render(request, "appsolver/index.html", context)
    elif request.method == "POST":
        theboard = request.session.get('theboard')
        guessword = request.POST["guessword"]
        if len(guessword) != WORDLEN:
            # also test if a valid guess word
            # if not return message and go back to 
            # return HttpResponseRedirect(reverse("guess"))
            messages.add_message(request, messages.INFO, "Invalid guess")
            return HttpResponseRedirect(reverse("index"))
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
        k = request.session.get('knowledge')
        k.update_knowledge(request.session.get('last_guess'), validateguess)
        
        request.session['theboard'] = theboard
        print('guess of ', validateguess, ' recorded')
        return HttpResponseRedirect(reverse("index"))
        
    else:
        theboard = request.session.get('theboard')
        context = {
            "theboard": theboard,
            "lowid": theboard.current_guess * WORDLEN,
            "highid": (theboard.current_guess + 1) * WORDLEN
        }
        return render(request, "appsolver/validate.html", context)
            

def register_new_user(request):
    newusername = 'user' + str(User.objects.all().count())
    user = User.objects.create_user(newusername)
    user.save()
    request.session['username'] = newusername
    clear_board_data(request)
    return newusername

def clear_board_data(request):
    request.session['all_words'] = readinwords()
    request.session['knowledge'] = initKnowledge()
    request.session['theboard'] = inittheboard()

# route clear
def clear(request):
    clear_board_data(request)
    messages.add_message(request, messages.INFO, "Board Cleared")
    return HttpResponseRedirect(reverse("index"))

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

