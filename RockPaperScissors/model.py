# Getting rock, paper and scissor options.
class RPS:
    ROCK = 'rock'
    PAPER = 'paper'
    SCISSOR = 'scissor'

    def get_choice(self):
        return (self.ROCK, self.PAPER, self.SCISSOR)

    def check_win(self, user1_choice, user2_choice):
        winner_check = {
            (RPS.ROCK, RPS.PAPER): False,
            (RPS.ROCK, RPS.SCISSOR): True,
            (RPS.PAPER, RPS.ROCK): True,
            (RPS.PAPER, RPS.SCISSOR): False,
            (RPS.SCISSOR, RPS.PAPER): True,
            (RPS.SCISSOR, RPS.ROCK): False,
        }

        won = None
        if user1_choice == user2_choice:
            won = None
        else:
            won = winner_check[(user1_choice, user2_choice)]

        return won
