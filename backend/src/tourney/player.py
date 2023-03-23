
from bots.bots import ChessBot
import time


class Player:
  def __init__(self, bot: ChessBot, friendly_name):
    self.id: int = None # Assigned at tourney level (At start tourney)
    self.friendly_name: str = friendly_name
    self.bot: ChessBot = bot
    self.elo: int = 800  # default Elo
    self.wins: int = 0
    self.losses: int = 0
    self.draws: int = 0

    # Game to game stats
    self.total_thinking_time: float = 0
    self.total_moves: int = 0

  def move(self, board):
    start_time = time.time()
    move = self.bot.make_move(board)
    self.total_thinking_time += time.time() - start_time
    self.total_moves += 1
    return move

  def __str__(self):
    return self.friendly_name