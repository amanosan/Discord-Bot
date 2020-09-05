from discord.ext import commands

from RockPaperScissors.parser import RockPaperScissorParser
from RockPaperScissors.model import RPS
from RockPaperScissors.controller import RPSGame

from Hangman.model import Hangman
from Hangman.controller import HangmanGame


class Games(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    
    @commands.command(
        usage='rock | paper | sciccor',
        brief='Play a game of Rock - Paper - Scissor',
        description=(
            "Choose between rock, paper and scissor and try to beat the Bot.\n"
            "The default user choice is ROCK."
        )
    )
    async def rps(self, ctx, user_choice: RockPaperScissorParser = RockPaperScissorParser(RPS.ROCK)):

        game_instance = RPSGame()

        user_choice = user_choice.choice
        won, bot_choice = game_instance.run(user_choice)

        if won is None:
            message = f"Both played - {user_choice.upper()}\nIt's a draw"
        elif won is True:
            message = f"The Bot played - {bot_choice.upper()}\nYou won !!"
        elif won is False:
            message = f"The Bot played - {bot_choice.upper()}\nYou lose :("

        await ctx.send(message)


    @commands.command(
        brief='Play a game of Hangman.',
        description=(
            "Just type in the command followed by your guess and guess the word.\n"
            "You will only get 10 chances so play carefully."
        )
    )
    async def hm(self, ctx, user_guess: str):
        player_id = ctx.author.id

        hangman_instance = HangmanGame()
        gameOver, won = hangman_instance.run(player_id, user_guess)

        if gameOver:
            gameOver_message = "You did not win."
            if won:
                gameOver_message = "Congrats you won."

            gameOver_message += f"The word was {hangman_instance.get_secret_word()}"

            # resetting the game for the player
            await hangman_instance.reset(player_id)
            await ctx.send(gameOver_message)

        else:

            await ctx.send(f"Progress: {hangman_instance.get_progress_string()}")
            await ctx.send(f"Guesses so far: {hangman_instance.get_guess_string()}")

        
def setup(bot):
    bot.add_cog(Games(bot))