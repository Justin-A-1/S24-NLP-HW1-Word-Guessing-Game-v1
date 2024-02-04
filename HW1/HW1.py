"""
JUSTIN AEGTEMA
HW 1 - WORD GUESS GAME

CODE FUNCTION: analyzes .txt file
- TASK 1: check for input
- TASK 2: calculates tokens, unique tokens, and lexical diversity
- TASK 3: a function that preprocesses raw text, including 
--- make lower-case, tokenize, remove non-alpha tokens,...
--- remove NLTK stopword list, remove length <=5,...
--- lemmatize tokens, use set() for unique lemmas,...
--- do pos tagging on unique lemmas, create list of nouns among them,...
--- print and return relevant results
- TASK 4:  make a dictionary { noun:count }, sort it by count,... 
--- ...and print the 50 most common nouns and their counts, and...
--- save these common words to a list
- TASK 5: guessing game
--- generates a word guess game based on the files content
--- adjust score based on correctness of guesses
--- outputs score and current game state to player

OUTPUT: 
- Lexical diversity (TASK 2)
- 20 tagged words, various tokens, various nouns (TASK 3)
- Word guess game
"""
import sys
import nltk
# print(nltk.data.path)
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('averaged_perceptron_tagger')
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from random import seed
from random import randint



# TASK 3 - function that preprocesses the raw text
def task3_preprocess_raw_text(raw_text):
    """
    CODE FUNCTION:
    --- make lower-case, tokenize, remove non-alpha tokens,...
    --- remove NLTK stopword list, remove length <=5,...
    --- lemmatize tokens, use set() for unique lemmas,...
    --- do pos tagging on unique lemmas, create list of nouns among them,...
    --- print and return relevant results

    OUTPUT:
    --- 20 tagged words, various tokens, various nouns
    """

    # TASK 3A
    # --- make lower-case, tokenize, remove non-alpha tokens,...
    # --- remove NLTK stopword list, remove length <=5
    raw_text_a1_lower = raw_text.lower()
    tokens_a2_tokenize = word_tokenize(raw_text_a1_lower)
    tokens_a3_alpha = [word for word in tokens_a2_tokenize if word.isalpha()]
    stopwords1 = set(stopwords.words('english'))
    tokens_a4_no_stopwords = [word for word in tokens_a3_alpha if word not in stopwords1]
    min_length = 6
    tokens_a5_min6 = [word for word in tokens_a4_no_stopwords if len(word) >= min_length]
    tokens_a_final = tokens_a5_min6

    # TASK 3B
    # --- lemmatize tokens, use set() for unique lemmas
    lemmatizer = WordNetLemmatizer()
    lemmas_b1 = [lemmatizer.lemmatize(word) for word in tokens_a_final]
    unique_lemmas_b2 = set(lemmas_b1)
    unique_lemmas_b_final = unique_lemmas_b2

    # TASK 3C
    # --- do pos tagging on unique lemmas
    # --- print the first 20 words and their tag
    pos_tagged_lemmas_c1 = nltk.pos_tag(unique_lemmas_b_final)
    # for word, tag in pos_tagged_lemmas_c1[:20]:
    #    print(word,tag)
    pos_tagged_lemmas_c_final = pos_tagged_lemmas_c1

    # TASK 3D
    # --- create a list of the pos tagged lemmas that are *nouns*
    nouns_d1 = [word for word, tag in pos_tagged_lemmas_c_final if tag.startswith('N')]
    nouns_d_final = nouns_d1

    # TASK 3E
    # --- print number of tokens from A and number of nouns from D
    print("Tokens from step a:", len(tokens_a_final))
    print("Nouns from step d:", len(nouns_d_final))

    # TASK 3F
    # --- return tokens_a_final and nouns_d_final
    return tokens_a_final, nouns_d_final



# TASK 5 - guessing game function
def guessing_game(word_list):
    """
    CODE FUNCTION:
    - create a guessing game based on the word_list
    - give players 5 starting points
    - lose 1 point per wrong letter guess
    - gain 1 point per correct guess
    - fill in the word as the player guesses correctly

    OUTPUT:
    - text displaying current score, correctness of last guess...
    ...current portion of word that has been guessed, etc

    """
    #initialize the game
    print("Let's play a word guessing game! New game starts now!")
    score = 5
    print(f"Starting score: {score}")

    # pick a random word
    # seed(1234) # allows for reproducibility
    rand_num = randint(0,49)
    word_to_guess = word_list[rand_num][0]
    # print for testing purposes
    # print(f"random choice #{rand_num}: {word_to_guess}") 
    # word_length = len(word_to_guess)
    guessed_letters_indices = [False]*len(word_to_guess) # track which letter indices have been guessed
    have_won = False # track if the game is won yet

    # core of the game
    # while loop runs until score is negative, user types "!" to leave...
    # ... or user correctly guesses all letters
    while score >= 0:

        # print blanks with correct letters filled in
        for i in range(len(word_to_guess)):
            # print(f"{i}",end='')
            if guessed_letters_indices[i] == True:
                print(f"{word_to_guess[i]}","", end="")
            else:
                print("_ ", end="")
        print("\n")

        # if game was won in the last loop, exit loop here, after printing the correct word
        if have_won == True:
            break

        # guess prompt
        user_input = input("Guess a letter:")

        # exit loop for "!" input
        if user_input == "!":
            break
        
        guessed_right = False # guessed_right gets switched to True if the guessed letter...
        #... occurs at least once in the word

        # tracks whether the guessed letter appears anywhere in the word, and if so...
        # ... tracks where it appeared
        for i in range(len(word_to_guess)):
            if word_to_guess[i] == user_input:
                guessed_letters_indices[i] = True
                guessed_right = True
        
        # print right/wrong, adjust score
        if guessed_right == True:
            score = score + 1
            print(f"Right! Score is {score}")
        if guessed_right == False:
                score = score - 1
                if score < 0:
                    break
                print(f"Sorry, guess again. Score is {score}")

        # if all letters have been guessed, the game is won
        if sum(guessed_letters_indices) == len(guessed_letters_indices):
            have_won = True

    # select appropriate end condition
    if user_input == "!":
        print("User exit (no win/loss)")
    elif have_won == False:
        print("You lost!")
        print(f"It was {word_to_guess}.")
    elif have_won == True:
        print("You solved it!")

def main():
    # TASK 1
    # if no system arg is present, print an error message and exit the program
    if len(sys.argv) < 2:
        print("ERROR: No input text file.")
        sys.exit()

    # TASK 2
    # 2a. read the input file as raw text
    # 2b. calculate the lexical diversity (unique tokens/total tokens)
    # 2c. print lexical diversity

    # 2a. read the input file as raw text
    filename = sys.argv[1] # use the file's name
    with open(filename,'r', encoding='utf-8') as file:
        raw_text = file.read()

    # 2b. calculate the lexical diversity (unique tokens/total tokens)
    tokens_list = word_tokenize(raw_text)
    # first_20_tokens = tokens_list[:20]
    # for token in first_20_tokens:
    #     print(token)
    unique_tokens = set(tokens_list)
    total_tokens_count = len(tokens_list)
    unique_tokens_count = len(unique_tokens)
    lexical_diversity = unique_tokens_count/total_tokens_count

    # 2c. print lexical diversity
    # print("Total tokens count:", total_tokens_count)
    # print("Unique tokens count:", unique_tokens_count)
    print("Lexical Diversity: {:.2f}".format(lexical_diversity))

    # TASK 3 - function that preprocesses the raw text
    tokens_3, nouns_3 = task3_preprocess_raw_text(raw_text)

    # TASK 4
    # --- make a dictionary { noun:count }, sort it by count,... 
    # --- ...and print the 50 most common nouns and their counts, and...
    # --- save these common words to a list

    # make a dictionary {noun:count}
    noun_count_dict_4a = {word: tokens_3.count(word) for word in nouns_3}

    # sort the dictionary by count
    sorted_noun_dict_4b = sorted(noun_count_dict_4a.items(), key=lambda item: item[1], reverse=True)

    # truncate list to just 50 items
    truncated_50_sorted_noun_dict_4c = sorted_noun_dict_4b[:50]

    # save the truncated list
    noun_dict_4_final = truncated_50_sorted_noun_dict_4c

    # print the 50 most common words
    print(noun_dict_4_final)

    # TASK 5 - guessing game function
    continue_game = True
    while(continue_game):
        guessing_game(noun_dict_4_final)
        user_input = input("Type \"y\" to play again, anything else to end:")

        # stop game if user does not enter "y"
        if user_input != "y":
            continue_game = False

if __name__ == "__main__":
    main()
