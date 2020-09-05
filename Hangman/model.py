class Hangman():
    word = ""
    progress_word = ""
    guesses = list()
    max_guesses = 10 

    def __init__(self, word):
        self.word = word
        self.guesses = list()

    def is_game_over(self, guess):
        gameOver = False
        won = False

        if self.check_guesses_left() == 0:
            gameOver = True

        won = self.check_guess_word(guess)

        if won:
            gameOver = True

        return gameOver, won


    def get_number_of_guesses(self):
        return len(self.guesses)


    def check_guesses_left(self):
        if self.get_number_of_guesses() >= self.max_guesses:
            return 0
        return self.max_guesses - self.get_number_of_guesses()


    def check_guess_word(self, word):
        if self.word == word:
            return True
        return False


    def guess(self, character):
        character = character.lower()

        self.progress_word = ""

        for c in self.word.lower():
            if c == character or c in self.guesses:
                self.progress_word += c
            else:
                self.progress_word +="\_."

        self.guesses.append(character)

