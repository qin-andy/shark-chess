from bots.chess_bot import ChessBot
import chess
import chess.engine

import random

class WaterBot(ChessBot):
  """
  Waters down any two bots by giving a random ratio of moves from one to the other
  The ratio is the chance of selecting move from b1, otherwise b2 is moved
  """
  code = 'WB'

  def __init__(self, b1: ChessBot, b2: ChessBot, water_ratio: float):
    super().__init__()
    self.b1 = b1
    self.b2 = b2

    self.settings.update({
        # TODO : could refactor to not inlcude settings fields for simple bots.
        'b1': b1.settings,
        'b2': b2.settings,
        'ratio': water_ratio
    })
    self.custom_name = None

  def make_move(self, board):
    move = chess.Move
    if random.random() <= self.settings['ratio']:
      move, comment = self.b1.make_move(board)
      return move, '+' + comment
    else:
      move, comment = self.b2.make_move(board)
      return move, '-' + comment

  def __str__(self):
    if self.custom_name == None:
      return 'W:[' + str(self.b1) + str(self.b2) + ']R:' + str(self.settings['ratio'])
    return self.custom_name


class SharkFishBot(ChessBot):
  """
  After capturing, gets excited and begins lurking, before entering a frenzy
  """
  code = 'SHR'

  def __init__(self, shallow_bot: ChessBot, lurk_time, frenzy_time,
               engine: chess.engine.SimpleEngine, limit):
    super().__init__()
    self.custom_name = None
    self.shallow_bot = shallow_bot  # todo : refactor to be settings compatible
    self.settings.update({
        'shallow bot': shallow_bot.code,
        'lurk time': lurk_time,
        'frenzy time': frenzy_time
    })
    self.excitement_time = 0
    self.engine = engine
    self.limit = limit

  def make_move(self, board):
    lurk_time = self.settings['lurk time']
    frenzy_time = self.settings['frenzy time']
    # Excitement Case
    if self.excitement_time > 0:
      if self.excitement_time <= frenzy_time:
        comment = 'frenzy[' + str(self.excitement_time) + ']'
        result = self.engine.play(board, self.limit)
        self.excitement_time -= 1
        return result.move, comment
      else:
        move, comment = self.shallow_bot.make_move(board)
        lurk_comment = 'lurk[' + str(self.excitement_time) + ']'
        comment = lurk_comment + ' --- ' + comment
        self.excitement_time -= 1
        return move, comment
    # Make a shallow move. If it's a check or capture, get excited
    move, comment = self.shallow_bot.make_move(board)
    if board.gives_check(move) or board.is_capture(move):
      self.excitement_time = lurk_time + frenzy_time
      comment = '!' + comment
    return move, comment

  def __str__(self):
    if self.custom_name == None:
      return 'Shark[' + str(self.shallow_bot) + ']R:' + str(self.limit)
    return self.custom_name
