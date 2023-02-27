# Helper that creates a random legal move
import random
import typing

import chess
import chess.engine


# Base chess bot
class ChessBot:
  def make_move(self, board: chess.Board) -> typing.Tuple[chess.Move, str]:
    pass

  def __str__(self):
    return "Base"


def move_rand(board: chess.Board) -> chess.Move:
  moves = board.generate_legal_moves()
  moves_arr = [move for move in moves]
  rand_move = random.choice(moves_arr)
  return rand_move


# Always random move bot
class AlwaysRandomBot(ChessBot):
  def make_move(self, board):
    return move_rand(board), ''

  def __str__(self):
    return "AlwaysRandom"


# Full Stockfish Bot
# Limit - thinking time in seconds
class Stockfish100Bot(ChessBot):
  def __init__(self, engine: chess.engine.SimpleEngine, limit):
    super().__init__()
    self.engine = engine
    self.limit = limit

  def make_move(self, board):
    comment = 'Stockfish' + str(self.limit.time)
    result = self.engine.play(board, self.limit)
    return result.move, comment

  def __str__(self):
    return "SF:" + str(self.limit)


# Water Bot
# Waters down any two bots by giving a random ratio of moves from one to the other
class WaterBot(ChessBot):
  def __init__(self, b1: ChessBot, b2: ChessBot, water_ratio: float):
    super().__init__()
    self.b1 = b1
    self.b2 = b2
    self.water_ratio = water_ratio
    self.custom_name = None

  def make_move(self, board):
    move = chess.Move
    if random.random() <= self.water_ratio:
      move, comment = self.b1.make_move(board)
      return move, '+' + comment
    else:
      move, comment = self.b2.make_move(board)
      return move, '-' + comment

  def __str__(self):
    if self.custom_name == None:
      return 'W:[' + str(self.b1) + str(self.b2) + ']R:' + str(self.water_ratio)
    return self.custom_name


# Always does moves which check. Then captures, then random after.
class BerserkBot(ChessBot):
  def make_move(self, board):
    checks_arr = [move for move in board.generate_legal_moves() if board.gives_check(move)]
    captures_arr = [move for move in board.generate_legal_moves() if board.is_capture(move)]
    moves_arr = [move for move in board.generate_legal_moves()]
    if checks_arr:
      return random.choice(checks_arr), 'Check'
    elif captures_arr:
      return random.choice(captures_arr), 'Capture'
    else:
      return random.choice(moves_arr), ''

  def __str__(self):
    return "Berserk"


# Prioitizes none-capturing moves.
class PacifistBot(ChessBot):
  def make_move(self, board):
    checks_arr = [move for move in board.generate_legal_moves() if board.gives_check(move)]
    captures_arr = [move for move in board.generate_legal_moves() if board.is_capture(move)]
    moves_arr = [move for move in board.generate_legal_moves()]
    safe_moves_arr = [move for move in moves_arr if
                      (not board.gives_check(move)) and (not board.is_capture(move))]
    if safe_moves_arr:
      return random.choice(safe_moves_arr), ''
    else:
      return random.choice(moves_arr), '!'

  def __str__(self):
    return "Pacifist"


# Prioitizes moving king (randomly)
class DanceKingBot(ChessBot):
  def make_move(self, board):
    moves_arr = [move for move in board.generate_legal_moves()]
    king_moves = [move for move in moves_arr if move.from_square == board.king(board.turn)]
    if king_moves:
      return random.choice(king_moves), '!'
    else:
      return random.choice(moves_arr), ''

  def __str__(self):
    return "DanceKing"


# Prioitizes moving king towards enemy king
class SuicideKingBot(ChessBot):
  def make_move(self, board):
    moves_arr = [move for move in board.generate_legal_moves()]
    king_moves = [move for move in moves_arr if move.from_square == board.king(board.turn)]
    target_square = board.king(not board.turn)  # Find opponent turn

    king_moves.sort(key=lambda x: chess.square_distance(x.to_square, target_square))
    if king_moves:
      curr_dist = chess.square_distance(board.king(board.turn), target_square)
      # If the closest king move would move it farther from the enemy king, pass
      if chess.square_distance(king_moves[0].to_square, target_square) >= curr_dist:
        return random.choice(moves_arr), ''
      return king_moves[0], '!'
    else:
      return random.choice(moves_arr), '?'

  def __str__(self):
    return "SuicideKing"


# Plays with Stockfish strength except when in check, then moves randomly
class PanicFishBot(ChessBot):
  def __init__(self, engine: chess.engine.SimpleEngine, limit):
    super().__init__()
    self.engine = engine
    self.limit = limit

  def make_move(self, board):
    if board.is_check():
      return move_rand(board), "!?"
    else:
      result = self.engine.play(board, self.limit)
      return result.move, ''

  def __str__(self):
    return "PanicFish"


# After capturing, gets excited and begins lurking, before entering a frenzy
class SharkFishBot(ChessBot):
  def __init__(self, shallow_bot: ChessBot, lurk_time, frenzy_time,
               engine: chess.engine.SimpleEngine, limit):
    super().__init__()
    self.custom_name = None
    self.shallow_bot = shallow_bot
    self.lurk_time = lurk_time
    self.frenzy_time = frenzy_time
    self.excitement_time = 0
    self.engine = engine
    self.limit = limit

  def make_move(self, board):
    # Excitement Case
    if self.excitement_time > 0:
      if self.excitement_time <= self.frenzy_time:
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
      self.excitement_time = self.lurk_time + self.frenzy_time
      comment = '!' + comment
    return move, comment

  def __str__(self):
    if self.custom_name == None:
      return 'Shark[' + str(self.shallow_bot) + ']R:' + str(self.limit)
    return self.custom_name
