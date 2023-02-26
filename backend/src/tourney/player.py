
from bots.bots import ChessBot


class Player:
  def __init__(self, bot: ChessBot, friendly_name):
    self.friendly_name = friendly_name
    self.bot = bot
    self.elo = 800  # default Elo
    self.wins = 0
    self.losses = 0
    self.draws = 0

  def move(self, board):
    return self.bot.make_move(board)

  def __str__(self):
    return self.friendly_name