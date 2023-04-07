# Base chess bot
import chess
import chess.engine
import typing

class ChessBot:
  code = '0'
  def __init__(self):
    # Bot code has two uses:
      # Used in exporting tourneys to record a player's bot type
      # Used on BotManager level to construct bots
    self.settings = { 'Code': self.code }

  def make_move(self, board: chess.Board) -> typing.Tuple[chess.Move, str]:
    pass

  def __str__(self):
    return "Base"