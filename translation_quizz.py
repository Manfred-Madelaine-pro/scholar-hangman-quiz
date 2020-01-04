import string
import random



# ------------------------------------ Static Variables ------------------------------------

MAX_ATTEMPTS = 3
UNKNOWN_CHAR = '_'
RANDOM_GUESS = False


# liste des languages possible
all_languages = ['French', 'Cat', 'Minion']
# dictionnaire_de_mot = { entier: {langue: mot} }
dico = {
    0: {all_languages[0]: 'quoi', all_languages[1]: 'miaou', all_languages[2]: 'kasa'},
    1: {all_languages[0]: 'bonjour', all_languages[1]: 'miaouhou', all_languages[2]: 'holala'},
    1: {all_languages[0]: 'mechant', all_languages[1]: 'kashii', all_languages[2]: 'papaya'}
}



# ------------------------------------ Languages ------------------------------------

def choose_language(languages):
    return random.choice(languages)

def choose_translation_language(languages, starting_language):
    l_copy = languages.copy()
    l_copy.remove(starting_language)
    return choose_language(l_copy)



# ------------------------------------ Words ------------------------------------

def choose_words(words_dico):
    return random.choice(words_dico)

def get_word(words, language):
    return words[language]

def guess_word(correct_w):
    print("Enter the translation:")
    if(RANDOM_GUESS):
        return guess_word_random(correct_w)
    return guess_word_user()

def guess_word_random(correct_w):
    return correct_w if random.random() > 0.5 else ""

def guess_word_user():
    word = input("\t> ")
    return word.lower()

def guess_letter():
    print("Enter the letter or the entire word:")
    if(RANDOM_GUESS):
        return guess_letter_random()
    return guess_letter_user()

def guess_letter_random():
    return(random.choice(string.ascii_lowercase))


def guess_letter_user():
    letter = input("\t> ")
    return letter.lower()



# ------------------------------------ Quizz ------------------------------------

def translation_quizz():
    intro_quizz()

    words = choose_words(dico)

    l_start = choose_language(all_languages)
    l_trans = choose_translation_language(all_languages, l_start)

    print_translation_language(l_start, l_trans)

    w_to_trans = get_word(words, l_start)
    correct_w = get_word(words, l_trans)

    print_translate_word(w_to_trans, l_start, l_trans)
    
    w_guessed = guess_word(correct_w)
    print_attempt(w_guessed)

    if (w_guessed != correct_w):
        print_fail_word()
        
        win = play_hangman(correct_w) 
        if (not win):
            return print_game_over()

    print_win()



# ------------------------------------ Pendu ------------------------------------

def play_hangman(correct_w):
    intro_hangman()

    misses = []
    complete_w = list(correct_w)
    uncomplete_w = [UNKNOWN_CHAR for _ in correct_w]

    while continue_hangman(len(misses), uncomplete_w):
        print_hangman(uncomplete_w, misses)

        letter = guess_letter()
        print_attempt(letter, type='letter' if (len(letter) == 1) else 'word')

        if is_correct_word(letter, correct_w):
            return True

        if letter in uncomplete_w:
            misses.append(letter)
            print_already_found()
        elif len(letter) == 1 and letter in complete_w:
            new_letters = 0
            for i, e in enumerate(correct_w):
                if letter == e:
                    new_letters += 1
                    uncomplete_w[i] = e
            print_correct_guess(new_letters)
        else:
            misses.append(letter)
            print_fail(letter, len(misses))

        print_end_of_turn()

    return UNKNOWN_CHAR not in uncomplete_w

def continue_hangman(fails, uncomplete_w):
    return (fails < MAX_ATTEMPTS) and (uncomplete_w.count(UNKNOWN_CHAR) > 0)

def is_correct_word(word, correct_word):
    return word == correct_word


# ------------------------------------ Prints ------------------------------------

def intro_quizz():
    print("\n--- Welcome to the Translation Quizz ! ---\n")

def intro_hangman():
    print("\n\n--- Try to find the word by playing Hangman ! ---\n")

def print_translation_language(l_start, l_trans):
    print("Translation language : {} --> {}.\n".format(l_start, l_trans))

def print_translate_word(w_to_trans, l_start, l_trans):
    print("Translate the word '{}' from {} to {}:".format(w_to_trans, l_start, l_trans))

def print_hangman(word, misses):
    print("Word   : {}".format(" ".join(word)))
    if (len(misses) > 0):
        print("Misses : {}".format(", ".join(misses)))
    print()

def print_attempt(guessing, type='word'):
    print("\nTrying the {} : '{}'.".format(type, guessing))

def print_correct_guess(new_letters):
    print("You have found {} new letter(s) !". format(new_letters))

def print_already_found():
    print("You have already found this letter !")
    
def print_fail(letter, fails):
    if(len(letter) > 1):
        print_fail_word()
    print_fail_letter(fails)
    print("Failing attempt n° {}/{}.".format(fails, MAX_ATTEMPTS))

def print_fail_letter(fails):
    error_messages = [
        "Your guess was incorrect...", 
        "This letter is unfortunately not in the word."
    ]
    print(random.choice(error_messages))

def print_fail_word():
    fail_messages = [
        "It's a fail !", 
        "Sorry but this word is incorrect !", 
        "It's not the correct translation, sorry !"
    ]
    print(random.choice(fail_messages))

def print_end_of_turn():
    end_of_turn_messages = [
        "-----------------------------------------------------",
        "-----------------------------------------------------",
        "~~~~~~~~~~~~~~~~~~~~~ (** ^ **) ~~~~~~~~~~~~~~~~~~~~~",
        "-----------------------------------------------------",
        "-----------------------------------------------------"
    ]
    print(random.choice(end_of_turn_messages) + "\n")

def print_game_over():
    loose_messages = [
        "You lost :'(...", 
        "game over ! You'll do better next time :D.", 
        "Look's like you're not very good at translation :(...", 
        "Ho, you lost again... This word was hard for me too you know."
    ]
    print_box(random.choice(loose_messages))

def print_win():
    win_messages = [
        "It's a win !", 
        "You found the correct translation !", 
        "Great, your guess was right !"
    ]
    print_box(random.choice(win_messages))


def print_box(text):
    padding = 5
    char_h = random.choice(['-', '+', '~', '='])
    char_v = random.choice(['|', 'I', 'T', 'M', 'V', 'U', 'X', 'H'])

    line = char_h * (len(text) + padding*2 + 2)
    blank_line = char_v + " " * (len(text) + padding*2) + char_v
    content = char_v + " "*padding + "{}" + " "*padding + char_v
    
    print(line)
    print(blank_line)
    print(content.format(text))
    print(blank_line)
    print(line)

def print_restart():
    print("would you like to restart ? (y/n)")



# ------------------------------------ Main ------------------------------------

def main():
    while "is playing":
        translation_quizz()

        if(not restart()):
            break
            
def restart():
    print_restart()
    response = input("\t> ")
    return True if (response.lower() in ['yes', 'oui', 'y', 'o']) else False


main()
