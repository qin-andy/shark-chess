# Result to store results from a game plaed
import math
import time

import chess
import chess.pgn

from src.bots.bots import ChessBot, WaterBot


class GameResult:
  def __init__(self):
    self.white_player = None
    self.black_player = None
    self.winner = None
    self.moves = None
    self.time = None
    self.pgn = None
    self.end_reason = None
    self.pc_game = None
    self.pc_board = None

  def __str__(self):
    result = ""
    result += "[" + self.white_player + "]" + " vs " + "[" + self.black_player + "]"
    return result


def create_game_result(wb: ChessBot, bb: ChessBot,
                       board: chess.Board, game: chess.pgn.Game):
  # Basic Naming
  gr = GameResult()
  gr.white_player = str(wb)
  gr.black_player = str(bb)
  gr.moves = board.fullmove_number

  game.headers['Event'] = "Bot Match"
  game.headers['White'] = str(wb)
  game.headers['Black'] = str(bb)

  gr.pgn = str(game)

  # For testing, remove later-
  gr.pc_board = board
  gr.pc_game = game

  # Outcome
  outcome = board.outcome()
  # No board outcome means turn limit was hit
  if outcome == None:
    gr.winner = 'Draw'
    gr.end_reason = 'Turn Limit'
  else:
    gr.end_reason = outcome.termination.name
    if outcome.winner == None:
      # No winner means stalement
      gr.winner = 'Stalemate'
    else:
      # Winner is either black or white bot
      if outcome.winner:
        gr.winner = str(wb)
      else:
        gr.winner = str(bb)
  return gr


# Play a single game between bots
def play_game(wb: ChessBot, bb: ChessBot, turn_limit: int):
  board = chess.Board()
  game = chess.pgn.Game()
  node = game
  turns = 0

  start_time = time.time()
  while not board.is_game_over() and turns <= turn_limit:
    move = None
    if board.turn:
      move, comment = wb.make_move(board)
    else:
      move, comment = bb.make_move(board)
    node = node.add_variation(move)
    node.comment = comment
    board.push(move)
    turns += 1
  game.end()
  game_result = create_game_result(wb, bb, board, game)
  game_result.time = time.time() - start_time
  return game_result


def generate_water_bots(b1, b2, name=None):
  mixes = [0.1, 0.2, 0.8, 0.9]
  water_bots = []
  for mix in mixes:
    water_bot = WaterBot(b1, b2, mix)
    if not name == None:
      water_bot.custom_name = name + str(int(mix * 100))
    water_bots.append(water_bot)
  return water_bots


def win_prob(rating1, rating2):
  return 1.0 * 1.0 / (1 + 1.0 * math.pow(10, 1.0 * (rating2 - rating1) / 400))
  # Geeks for geeks was wrong..... their version has a typo int he above alg


# Takes 1 ELO,s a K value, and d = winner == 1
def calculate_elos(rating1, rating2, K, d):
  prob1 = win_prob(rating1, rating2)
  prob2 = win_prob(rating2, rating1)
  # print(prob1, prob2)
  # Case -1 When Player A wins
  if (d == 1):
    rating1 += K * (1 - prob1)
    rating2 += K * (0 - prob2)

  # Case -2 When Player B wins
  elif (d == 0):
    rating1 += K * (0 - prob1)
    rating2 += K * (1 - prob2)

  # Tie case
  else:
    rating1 += K * (0.5 - prob1)
    rating2 += K * (0.5 - prob2)

  return int(rating1), int(rating2)


elo_k = 32  # Determines how much Elo goes up and down


# Actually play the games

# Helper to play multiple games between two bots
def multiplay(wb, bb, count, elos=None):
  grs = []  # game results array
  for i in range(count):
    print('Game [' + str(i + 1) + '/' + str(count) + "] of [" + str(wb) + "] vs [" + str(bb) + "]")
    gr = play_game(wb, bb, 300)
    print(gr.winner + ' wins in [' + str(gr.moves) + '] turns in [' + str(gr.time) + '] seconds')
    if elos:  # Update Elos case
      if str(wb) == str(bb):
        pass
      else:
        winner = 0.5
        if (gr.winner == str(wb)):
          winner = 1
        elif (gr.winner == str(bb)):
          winner = 0
        elos[str(wb)], elos[str(bb)] = calculate_elos(elos[str(wb)], elos[str(bb)], elo_k, winner)
        print(str(wb) + ': ' + str(elos[str(wb)]) + ', ' + str(bb) + ': ' + str(elos[str(bb)]))
    grs.append(gr)
  return grs


"""## Run Single Bot Match"""


def play_match(b1, b2, games_count, swap_colors=True, elos=None):
  print('=========<' + str(b1) + ' [vs] ' + str(b2) + '>=========')
  # Time and play games
  start_time = time.time()
  grs = []

  grs += multiplay(b1, b2, games_count, elos)
  if swap_colors:
    grs += multiplay(b2, b1, games_count, elos)  # switch colors
  end_time = time.time()
  print('Total Time: ' + str((end_time - start_time)))
  print()

  return grs


# Play round robin tourney
def play_tournament(bots, match_length, swap_colors, elos):
  start_time = time.time()
  match_total = len(bots) ** 2
  match_count = 0
  grs = []
  for b1 in bots:
    for b2 in bots:
      match_count += 1
      # Play a single one-sided match (no color swapping)
      print('Match ' + str(match_count) + '/' + str(match_total))
      grs += play_match(b1, b2, match_length, swap_colors, elos)
  total_time = time.time() - start_time
  print('Total time for tournament: ' + str(total_time))
  return grs
