
from bots.bots import ChessBot


class Player:
  def __init__(self, bot: ChessBot, friendly_name):
    self.id: int = None # Assigned at tourney level (At start tourney)
    self.friendly_name: str = friendly_name
    self.bot: ChessBot = bot
    self.elo: int = 800  # default Elo
    self.wins: int = 0
    self.losses: int = 0
    self.draws: int = 0

  def move(self, board):
    return self.bot.make_move(board)

  def __str__(self):
    return self.friendly_name