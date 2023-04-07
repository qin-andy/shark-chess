# Base chess bot
import chess
import chess.engine
import typing

class ChessBot:
  code = '0'

  def __init__(self):
    """
    Initalizes a default chess bot. Populates settings with its bot code
      1. Used in exporting tourneys to record a player's bot type
      2. Used on BotManager level to construct bots
    """
    self.settings = {'Code': self.code}

  def make_move(self, board: chess.Board) -> typing.Tuple[chess.Move, str]:
    """
    Uses information from the board to create a chess move.
    """
    pass

  def __str__(self):
    return "Base"
