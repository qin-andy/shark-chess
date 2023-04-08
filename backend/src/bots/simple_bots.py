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


class AlwaysRandomBot(ChessBot):
  """
  Always random move bot
  """
  code = 'AR'

  def __init__(self):
    super().__init__()

  def make_move(self, board):
    return move_rand(board), ''

  def __str__(self):
    return "AlwaysRandom"


#
class Stockfish100Bot(ChessBot):
  """
  Full Stockfish Bot
  """
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


class BerserkBot(ChessBot):
  """
  Always does moves which check. Then captures, then random after.
  """
  code = 'BRK'

  def __init__(self):
    super().__init__()

  def make_move(self, board):
    checks_arr = [move for move in board.generate_legal_moves()
                  if board.gives_check(move)]

    if checks_arr:
      return random.choice(checks_arr), 'Check'
    
    captures_arr = [move for move in board.generate_legal_moves()
                if board.is_capture(move)]
    if captures_arr:
      return random.choice(captures_arr), 'Capture'
    
    moves_arr = [move for move in board.generate_legal_moves()]
    return random.choice(moves_arr), ''

  def __str__(self):
    return "Berserk"


class PacifistBot(ChessBot):
  """
  Prioitizes none-capturing moves.
  """
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

class DanceKingBot(ChessBot):
  """
  Prioitizes moving king (randomly)
  """
  code = 'DK'

  def __init__(self):
    super().__init__()

  def make_move(self, board):
    moves_arr = [move for move in board.generate_legal_moves()]
    king_moves = [
        move for move in moves_arr if move.from_square == board.king(board.turn)]
    if king_moves:
      return random.choice(king_moves), '!'
    else:
      return random.choice(moves_arr), ''

  def __str__(self):
    return "DanceKing"


class SuicideKingBot(ChessBot):
  """
  Prioitizes moving king towards enemy king
  """
  code = 'SK'

  def __init__(self):
    super().__init__()

  def make_move(self, board):
    moves_arr = [move for move in board.generate_legal_moves()]
    king_moves = [
        move for move in moves_arr if move.from_square == board.king(board.turn)]
    target_square = board.king(not board.turn)  # Find opponent turn

    king_moves.sort(key=lambda x: chess.square_distance(
        x.to_square, target_square))
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


class PanicFishBot(ChessBot):
  """
  Plays with Stockfish strength except when in check, then moves randomly
  """
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


class SensitiveFish(ChessBot):
  """
  Plays with Stockfish strength except when in check or when a piece is captured, then moves randomly
  """
  code = 'SNS'

  def __init__(self, engine: chess.engine.SimpleEngine, limit):
    super().__init__()
    self.engine = engine
    self.limit = limit

  def make_move(self, board: chess.Board):
    # this includes own captures.
    if (board.is_check()):
      return move_rand(board), "!?"
    
    # Check last move
    if len(board.move_stack) > 0:
      last_move = board.pop()
      is_last_move_capture = board.is_capture(last_move)
      board.push(last_move)

      if (is_last_move_capture):
        return move_rand(board), "!??"
    result = self.engine.play(board, self.limit)
    return result.move, ''

  def __str__(self):
    return "SensitiveFish"
