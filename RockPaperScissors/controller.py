from .model import RPS
import random
import datetime


class RPSGame:
    def run(self, user_choice):
        random.seed(datetime.datetime.now())
        rps_instance = RPS()

        if user_choice not in rps_instance.get_choice():
            raise Exception("Need either rock, paper or scissor.")
        
        bot_choice = random.choice(rps_instance.get_choice())

        # checking for winner:
        won = rps_instance.check_win(user_choice, bot_choice)

        return won, bot_choice