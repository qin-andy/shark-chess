import time

import chess
import chess.pgn
import pandas as pd

from src.bots.bots import ChessBot
from src.tourney.elo import calculate_elos


class Player:
  def __init__(self, bot: ChessBot, friendly_name):
    self.friendly_name = friendly_name
    self.bot = bot
    self.elo = 800  # default Elo

  def move(self, board):
    return self.bot.make_move(board)

  def __str__(self):
    return self.friendly_name


class GameResult:
  def __init__(self):
    self.white_player: str = None
    self.black_player: str = None
    self.winner: str = None
    self.r: float = None  # numerical value representing result. 1=w, 0.5=d, 0=b
    self.moves: int = None
    self.time: float = None
    self.pgn: str = None
    self.end_reason: str = None
    self.pc_game = None
    self.pc_board = None

  def update(self, wp: Player, bp: Player,
             board: chess.Board, game: chess.pgn.Game):
    # Basic Naming
    self.white_player = str(wp)
    self.black_player = str(bp)
    self.moves = board.fullmove_number

    game.headers['Event'] = "Bot Match"
    game.headers['White'] = str(wp)
    game.headers['Black'] = str(bp)

    self.pgn = str(game)

    # For testing, remove later-
    self.pc_board = board
    self.pc_game = game

    # Outcome logic
    outcome = board.outcome()
    # No board outcome means turn limit was hit
    if outcome is None:
      self.winner = 'Draw'
      self.end_reason = 'Turn Limit'
    else:
      self.end_reason = outcome.termination.name
      if outcome.winner is None:
        # No winner means stalemate
        self.winner = 'Stalemate'
        self.r = 0.5
      else:
        # Winner is either black or white bot
        if outcome.winner:
          self.winner = str(wp)
          self.r = 1
        else:
          self.winner = str(bp)
          self.r = 0
    return self

  def __str__(self):
    result = ""
    result += self.white_player + " vs " + self.black_player
    return result


class TourneyManager:
  def __init__(self, players: list[Player], match_length: int):
    self.concluded = False
    self.players = players
    self.match_length = match_length
    self.game_results: list[GameResult] = []

  # Play a single game between players
  def play_game(self, wp: Player, bp: Player, turn_limit: int):
    board = chess.Board()
    game = chess.pgn.Game()
    node = game
    turns = 0

    start_time = time.time()
    while not board.is_game_over() and turns <= turn_limit:
      move = None
      if board.turn:
        move, comment = wp.move(board)
      else:
        move, comment = bp.move(board)
      node = node.add_variation(move)
      node.comment = comment
      board.push(move)
      turns += 1
    game.end()
    game_result = GameResult()
    game_result.update(wp, bp, board, game)
    game_result.time = time.time() - start_time
    return game_result

  # Actually play the games
  def update_elos(self, wp: Player, bp: Player, d, elo_k=32):
    if str(wp) == str(bp):
      return

    wp.elo, bp.elo = calculate_elos(wp.elo, bp.elo, elo_k, d)
    print(str(wp) + ': ' + str(wp.elo) + ', ' + str(bp) + ': ' + str(bp.elo))

  # Helper to play multiple games between two bots
  def play_match(self, p1: Player, p2: Player, count, swap_colors=False):
    print('=========<' + str(p1) + ' [vs] ' + str(p2) + '>=========')

    # Time and play games
    start_time = time.time()
    elo_k = 32  # elo_k = 32, TODO: read from options
    grs = []  # game results array

    for i in range(count):
      print('Game [' + str(i + 1) + '/' + str(count) + "] of [" + str(p1) + "] vs [" + str(p2) + "]")
      gr = self.play_game(p1, p2, 300)
      print(gr.winner + ' wins in [' + str(gr.moves) + '] turns in [' + str(gr.time) + '] seconds')
      self.update_elos(p1, p2, gr.r, elo_k)
      grs.append(gr)

    if swap_colors:  # TODO: Recursive case, could be cleaner
      grs2 = self.play_match(p2, p1, count, False)
      grs += grs2

    print('Total Time: ' + str(time.time() - start_time))
    print()

    return grs

  # Play round robin tourney
  def play_tournament(self):
    players = self.players
    match_length = self.match_length

    start_time = time.time()
    match_total = len(players) ** 2
    match_count = 0
    grs = []
    for p1 in players:
      for p2 in players:
        match_count += 1
        # Play a single one-sided match (no color swapping)
        print('Match ' + str(match_count) + '/' + str(match_total))
        grs += self.play_match(p1, p2, match_length, False)
    total_time = time.time() - start_time
    print('Total time for tournament: ' + str(total_time))
    return grs

  def to_csv(self) -> str:
    if not self.concluded:
      return ""
    winners = []
    reasons = []
    moves = []
    times = []
    pgns = []
    whites = []
    blacks = []

    # Unzip array of game objects into arrays
    for gr in self.game_results:
      winners.append(gr.winner)
      reasons.append(gr.end_reason)
      moves.append(gr.moves)
      times.append(gr.time)
      pgns.append(gr.pgn)
      whites.append(gr.white_player)
      blacks.append(gr.black_player)

    # Settingup data in dict
    game_data = {
      'Winner': winners,
      'End Reason': reasons,
      'Moves': moves,
      'Time': times,
      'PGN': pgns,
      'White': whites,
      'Black': blacks
    }
    df = pd.DataFrame(game_data)
    df.to_csv('output.csv', encoding='utf-8-sig')
    # files.download('output.csv')

