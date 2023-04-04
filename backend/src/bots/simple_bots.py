# Helper that creates a random legal move
import random

import chess
import chess.engine


from bots.chess_bot import ChessBot


def move_rand(board: chess.Board) -> chess.Move:
  moves = board.generate_legal_moves()
  moves_arr = [move for move in moves]
  rand_move = random.choice(moves_arr)
  return rand_move


# Always random move bot
class AlwaysRandomBot(ChessBot):
  code = 'AR'
  def __init__(self):
    super().__init__()

  def make_move(self, board):
    return move_rand(board), ''

  def __str__(self):
    return "AlwaysRandom"


# Full Stockfish Bot
# Limit - thinking time in seconds
class Stockfish100Bot(ChessBot):
  code = 'SF'
  def __init__(self, engine: chess.engine.SimpleEngine, limit: chess.engine.Limit):
    super().__init__()
    self.engine = engine
    self.limit = limit

  def make_move(self, board):
    comment = 'Stockfish' + str(self.limit.time)
    result = self.engine.play(board, self.limit)
    return result.move, comment

  def __str__(self):
    return "SF:" + str(self.limit)


# Always does moves which check. Then captures, then random after.
class BerserkBot(ChessBot):
  code = 'BRK'
  def __init__(self):
    super().__init__()

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
  code = 'PC'
  def __init__(self):
    super().__init__()
  
  def make_move(self, board):
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
  code = 'DK'
  def __init__(self):
    super().__init__()

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
  code = 'SK'
  def __init__(self):
    super().__init__()

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
  code = 'PF'
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
  
# Plays with Stockfish strength except when in check or when a piece is captured, then moves randomly
class SensitiveFish(ChessBot):
  code = 'SNS'
  def __init__(self, engine: chess.engine.SimpleEngine, limit):
    super().__init__()
    self.engine = engine
    self.limit = limit

  def make_move(self, board: chess.Board):
    if (board.is_check()) or (board.halfmove_clock == 0): # this includes own captures.
      return move_rand(board), "!?"
    else:
      result = self.engine.play(board, self.limit)
      return result.move, ''

  def __str__(self):
    return "SensitiveFish"

