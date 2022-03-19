# WORDLE-SOLVE

## Introduction

This project was intended to satisfy the final or capstone project for CS50 Web Programming with Python and Javascript.

**Functionality:**

- The application helps the user solve Wordle puzzles. Wordle is a popular New York Times games feature. It is accessible at `https://www.nytimes.com/games/wordle/index.html`.  Wordle-Solve builds on the Wordle functionality in two ways.

  - First, it accommodates puzzles of multiple word lengths. The NYT Wordle only applies to words of five letters.

  - Second, it accommodates puzzles allowing more than 6 guesses. NYT Wordle is fixed in allowoing only six guesses.

  - Third, and related to point one, it includes functionalitly to take advantage of a much larger dictionary than the one used by the NYT Wordle. The NYT Wordle appears to use a fixed dictionary or lexicon of five-letter words that is accessiable from the javascript available for download from the NY Times website.

- The additional functionality of Wordle-Solve can be viewed and tested at sites such as `https://hellowordl.net/#`, which provides Wordle-like functionality but with the ability to create puzzles of different word lengths.

- The app is mobile-friendly and allows use on a smaller phone or other device.

**Distinctiveness and Complexity:**

The author believes there were two principal complex and interesting issues in implementing this application.

- First, it took significant thought and planning to develop algorithms capable of solving Wordle puzzles. As described below, two algorithms were developed, although only one proved performant enough for inclusion here.
  
- Second, I think the app faithfully executes the Django philosophy in its data connections between the python server code and the `javascript` and `html` code in the templates. In some cases, it might have been easier if everything could have been implemented in `javascript`, but it was enjoyable to see how the Django framework can create the same functionality.

## Technologies

The app is implements using Python3, Javascript, and the Django framework. The present version of the app uses the sqlite database.

## File Structure

- Key Python modules

  - `views.py` Includes code for generating/interpreting web pages and performing processing on them

  - `wordle-init.py` Initializes the board and knowledge structures

  - `wordle-solve.py` Class definitions for the board and knowledge classes and methods

- Templates

  - `base.html` Base page including navbar.

  - `board.html` Generate the board image

  - `index.html` Show suggested guesses and allow entry

  - `settings.html` Change settings

  - `validate.html` Allow entry of feedback from Wordle app

## Data Structure

### Database

The app uses Django's built-in support for modeling database tables and functions. Th app implements the following tables:

    class BigDWord(models.Model)
        word_text = models.CharField(max_length=50)
        word_length = models.SmallIntegerField(null=True)
        word_alpha = models.BooleanField(null=True)  

`BigDWord` *holds the very large dictionary downloaded from `https://github.com/dwyl/english-words` and includes hundreds of thousands of words of all lengths. Some words are not entirely alphabetical (for example, they include hypens). The app excludes those non-alpha words.*

    class WordleWord(models.Model):
        word_text = models.CharField(max_length=50)

`WordleWord`*holds the smaller 5-word Wordle dictionary, which I downloaded from the Wordle website on February 22, 2022.*

The app was originally written using SQLITE3 database but has been upgraded to support POSTGRESQL and migration to the `heroku` service. (See `wordle-solver-cox.herokuapp.com`).

### Session

The app uses session storage to hold parts of the dictionaries applicable to each user. By using session storage, the app avoids interference with users' individual sessions using the app. The app configures session storage to be stored using the database.

## How to Use

- As a django app, the app can be started using the development server by typing `python3 manage.py runserver` from the home directory of the app.

- The base home page includes a copy of the current Wordle board (which is blank to start with), an input field to type a word guess, and a list of "top suggested guesses" at the bottom.

- The user typically will open both the Wordle site and the Wordle-Solve site on separate halves of the display.

- The user selects a word from Wordle-Solve appe's "top suggested guesses" and clicks on it. It is automatically filled in in the "Your Guess" box. Then the user clicks "Submit" to populate the word in the Wordle-Solve board.

- The user then enters that word on the actual Wordle site and views the Wordle site's response as a series of colored boxes around each of the word's letters: Black (not in word), Yellow (in word but not in correct position), and Green (in word at correct position).

- The user enters the colored box information from Wordle in the Wordle-Solve application by clicking boxes to change their colors to match Wordle and then clicks the `Validate` button

  - note that sometimes, when the larger dictionary is selected, Wordle-Solve may suggest a guess word that isn't accepted by the Wordle site. In that case, the app provides a button to `Delete a word Wordle doesn't recognize`.

- After the user clicks `Validate`, the app then incorporates the feedback into its store of "knowledge" and then returns to the guess page with new word guess suggestions.

### Other features

- *Settings* - The user can change the word length, the number of guesses, and the dictionary to be used.

- *Clear Board* - The user can clear the current board

## How It Works

- The program uses the python3 class `WordKnowledge` to capture all of the feedback the user has input from the Wordle program's responses. For each letter of the puzzle, the program tracks which letters have been confirmed (G), ruled out (B), or still remain possibilities. It separately keeps track of letters that are mandatory (Y) but whose position hasn't been determined yet.

- The program also keeps a current list of all possible words `validWords` that satisfy the `WordKnowledge` requirements.

- The program includes two methods for selecting new guesses, although for performance reasons only one method is presently allowed.

  - The allowed method is a character-frequency count.

    - The program counts the frequencies of all letters in the remaining `valid_words`.

    - The program scores each `valid_word` by summing the counts for each of that word's letters.

    - The guesses are the word or words with the highest score.

  - The program includes an implementation of another method, the 'dynamic max elimination' method. 

    - For each word in the `valid_words` list, the program updates a temporary copy of the `WordKnowledge` assuming that word is the solution to the puzzle. 

    - It then recalculates the number of `valid_words` based on that assumption. 

    - Each possible `valid_word` is scored by noting how many words would be eliminated from the `valid_words` list if that word is, in fact, the secret. 

    - The guess is the word with the highest score (or if words are tied for the max, a random selection from these words).

  - The dynamic elimination method, however, did not prove to be performant for valid words lists of more than a few hundred, so it is not permitted in the executing code.

    - In my experience, the dynamic max elimination method, when activated, outperformed the character-frequency count method, but only by a very small margin.

## Results

In my experience, the program generally solves 5-letter Wordles in four or five guesses. Perhaps surprisingly, longer Wordles seem to be easier than shorter ones.
