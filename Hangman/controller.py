from .model import Hangman

import random

games = {}

class HangmanGame:

    current_game = None

    # function to get the word currently in the game.
    def get_secret_word(self):
        return self.current_game.word

    # function to get the guesses of the player
    def get_guess_string(self):
        return ",".join(self.current_game.guesses)

    # function to get the progress that the player has made
    def get_progress_string(self):
        return self.current_game.progress_word

    def get_game(self, player_id):
        if player_id in games.keys():
            self.current_game = games[player_id]
            if self.current_game is None:
                self.create_game(player_id)
        else:
            self.create_game(player_id)

    # function to get a random word.
    def get_random_word(self):
        words_choice = (
            'discord',
            'development',
            'python'
            'laptop'
        )
        return random.choice(words_choice)


    # function to create a game for a player.
    def create_game(self, player_id):
        self.current_game = Hangman(self.get_random_word())
        self.save(player_id)

    # function to save the game of a player.
    def save(self, player_id):
        games[player_id] = self.current_game

    # function to reset the game of a player.
    async def reset(self, player_id):
        games.pop(player_id)

    # function to run the game.
    def run(self, player_id, guess):
        self.get_game(player_id)
        is_game_over, won = self.play_round(guess)
        self.save(player_id)

        return is_game_over, won

    def play_round(self, guess):
        isWord = False
        if len(guess) == 1:
            pass
        elif len(guess) > 1:
            isWord = True
        else:
            return None, None

        if not isWord:
            self.current_game.guess(guess)

        is_game_over, won = self.current_game.is_game_over(guess)
        return is_game_over, won
        