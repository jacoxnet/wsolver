from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render
from django.contrib import messages
from django.urls import reverse

from .wordle_init import WORDLEN, GUESSLEN, register_new_user, clear_board_data

# Create your views here. 

# route /
def index(request):
    if request.method == "GET":
        # reset session data
        print('board is ', WORDLEN, 'by ', GUESSLEN, ', NYTimes dict ')
        username = register_new_user(request)
        print('your username is ', username)
        clear_board_data(request)
        return HttpResponseRedirect(reverse('guess'))
        
    elif request.method == "POST":
        # This handles original submission of a new guess word
        theboard = request.session.get('theboard')
        guessword = request.POST["guessword"]
        if len(guessword) != WORDLEN:
            # also test if a valid guess word
            # if not return message and go back to 
            # return HttpResponseRedirect(reverse("guess"))
            messages.add_message(request, messages.INFO, "Invalid guess")
            return HttpResponseRedirect(reverse("guess"))
        guessword = guessword.upper()
        print('adding', guessword, ' to board at position ', theboard.current_guess)
        for i in range(WORDLEN):
            theboard.board[theboard.current_guess][i].letter = guessword[i]
            theboard.board[theboard.current_guess][i].color = 'B'            
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
        # this handles validation of a guess once color codes are
        # entered and it's time to update knowledge
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
        k.updateValidWordList()
        request.session['valid_words'] = k.valid_words
        request.session['theboard'] = theboard
        print('guess of ', validateguess, ' recorded')
        return HttpResponseRedirect(reverse("guess"))
        
    else:
        # request method GET - handles calculating template for color
        # selection
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
        # this handles submission of guess words
        k = request.session.get('knowledge')            
        valid_words = k.valid_words
        print('retrieved', len(valid_words), ' valid words')
        nowords = False
        solved = False
        if len(valid_words) == 0:
            nowords = True
        elif len(valid_words) == 1:
            solved = True
        else:
            nowords = False
        theboard = request.session.get("theboard")
        if theboard.current_guess >= theboard.guesslen:
            noguesses = True
        else:
            noguesses = False
        context = {
            "theboard": theboard,
            "solved": solved,
            "topwords": k.nextGuess(),
            "nowords": nowords,
            "noguesses": noguesses,
            "lowid": theboard.current_guess * WORDLEN,
            "highid": (theboard.current_guess + 1) * WORDLEN
        }
        return render(request, "appsolver/index.html", context)    
    if request.method == "POST":
        # comes here on deleting a valid word
        delword = request.POST["delword"]
        if delword == "":
            print("didnt' get delword")
        if delword != "":
            print("trying to delete", delword)
            new_valid_words = request.session.get("valid_words").remove(delword)
            request.session["valid_Words"] = new_valid_words
        return HttpResponseRedirect(reverse("guess"))

# route clear
def clear(request):
    clear_board_data(request)
    messages.add_message(request, messages.INFO, "Board Cleared")
    return HttpResponseRedirect(reverse("index"))