class Hangman:

    def __init__(self):
        pass

    def __str__(self):
        pass

    def word_key(self, word, letter):

        key = ""
        for i in range(0, len(word)):
            if word[i] == letter:
                key += letter
            else:
                key += "-"
        return key

    def shortlist(self, words, letter):

        word_bins = {}
        for word in words:
            key = self.word_key(word, letter)
            if key in word_bins:
                word_bins[key].append(word)
            else:
                word_bins[key] = [word]

        max_bin = list(word_bins)[0]
        for key in word_bins:
            if len(word_bins[key]) > len(word_bins[max_bin]):
                max_bin = key
            elif len(word_bins[key]) == len(word_bins[max_bin]) and key.count("-") > max_bin.count("-"):
                max_bin = key
        return max_bin, word_bins[max_bin]

    def play(self):

        game_over = False
        ALPHABETS = "abcdefghijklmnopqrstuvwxyz"
        guessed_letters = []

        with open("dictionary.txt") as file:
            word_lengths = {len(line.rstrip()) for line in file}

        word_length = "Invalid Integer"
        while word_length == "Invalid Integer":
            try:
                word_length = int(input("Positive Integer Input | Word Length: "))
                if word_length <= 0 or word_length not in word_lengths:
                    print("\nSorry, there were no words that were", word_length, "letters long.\nThe possible word lengths are shown below.\n", word_lengths, "\nPlease try again.\n")
                    word_length = "Invalid Integer"
            except ValueError:
                pass

        with open("dictionary.txt") as file:
            word_list = [line.rstrip() for line in file if len(line.rstrip()) == word_length]

        guess_word = "-"*word_length

        guesses_remaining = "Invalid Integer"
        while guesses_remaining == "Invalid Integer":
            try:
                guesses_remaining = int(input("\nPositive Integer Input | Number Of Guesses: "))
                if guesses_remaining <= 0:
                    guesses_remaining = "Invalid Integer"
            except ValueError:
                pass

        show_words = "Not Boolean"
        while show_words == "Not Boolean":
            show_words = input("\nDo you want to see the remaining words? Yes or No: ")
            if show_words in ["Yes", "yes", "Y", "y"]:
                show_words = True
            elif show_words in ["No", "no", "N", "n"]:
                show_words = False
            else:
                show_words = "Not Boolean"

        while not game_over:

            print("\nGuesses Remaining:", guesses_remaining, "\nLetters guessed:", guessed_letters)
            if show_words:
                print("Possible Words Remaining:", word_list)


            guess_letter = "Invalid Guess"
            while guess_letter == "Invalid Guess":
                guess_letter = input("Guess a letter: ")
                if len(guess_letter) == 1 and guess_letter in ALPHABETS and guess_letter not in guessed_letters:
                    guessed_letters.append(guess_letter)
                else:
                    guess_letter = "Invalid Guess"

            shortlist = self.shortlist(word_list, guess_letter)
            word_list = shortlist[1]

            updated_guess_word = ""
            for i in range(0, word_length):
                if shortlist[0][i] != "-":
                    updated_guess_word += shortlist[0][i]
                else:
                    updated_guess_word += guess_word[i]
            guess_word = updated_guess_word

            print("\nWord:", guess_word)

            if shortlist[0] == "-"*word_length:
                guesses_remaining -= 1

            if len(word_list) == 1 and guess_word == word_list[0]:
                game_result = "Player Wins"
                game_over = True
            if guesses_remaining == 0:
                game_result = "Computer Wins"
                game_over = True

        if game_result == "Player Wins":
            print("\nCongratulations! You win!\n")
        else:
            print("\nYou are out of guesses! You lose!\nThe correct word was:", word_list[0], "\n")