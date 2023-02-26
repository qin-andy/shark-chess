import time

import chess
import chess.pgn
import pandas as pd
import os

from bots.bots import ChessBot
from tourney.elo import calculate_elos
from tourney.game_result import GameResult
from tourney.player import Player


class TourneyManager:
  def __init__(self, players: list[Player], match_length: int):
    self.concluded = False # TODO : remove or refactor
    self.players = players
    self.match_length = match_length
    self.elo_k = 32
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
      if comment != '': # empty comments mean no comment (!)
        node.comment = comment
      board.push(move)
      turns += 1
    game.end()
    game_result = GameResult()
    game_result.update(wp, bp, board, game)
    game_result.time = time.time() - start_time
    return game_result
  
  def update_player_data(self, wp: Player, bp: Player, gr: GameResult):
    # Updates player ELO, wins, losses, draws after reuslt

    d = 0 # default
    if gr.winning_color == 'white':
      d = 1 # for elo calc
      wp.wins += 1
      bp.losses += 1
    elif gr.winning_color == 'black':
      d = 0 # for elo calc
      wp.losses += 1
      bp.wins += 1
    else: # draw case
      d = 0.5
      bp.draws += 1
      wp.draws += 1 

    wp.elo, bp.elo = calculate_elos(wp.elo, bp.elo, self.elo_k, d)
    print(str(wp) + ': ' + str(wp.elo) + ', ' + str(bp) + ': ' + str(bp.elo))
  

  # Helper to play multiple games between two bots
  def play_match(self, p1: Player, p2: Player, count, swap_colors=False):
    print('=========<' + str(p1) + ' [vs] ' + str(p2) + '>=========')

    # Time and play games
    start_time = time.time()
    grs = []  # game results array

    for i in range(count):
      print('Game [' + str(i + 1) + '/' + str(count) + "] of [" + str(p1) + "] vs [" + str(p2) + "]")
      gr = self.play_game(p1, p2, 300)
      print(gr.winning_player + ' wins in [' + str(gr.moves) + '] turns in [' + str(gr.time) + '] seconds')
      self.update_player_data(p1, p2, gr)
      grs.append(gr)

    if swap_colors:  # TODO: Recursive case, could be cleaner
      grs2 = self.play_match(p2, p1, count, False)
      grs += grs2

    print('Total Time: ' + str(time.time() - start_time))
    print()

    return grs

  # Play round robin tourney
  # Skips mirror matches
  def play_tournament(self):
    players = self.players
    match_length = self.match_length

    start_time = time.time()
    match_total = (len(players) ** 2)- len(players)
    match_count = 0
    grs = []
    for p1 in players:
      for p2 in players:
        if str(p1) != str(p2): #skip self play matches
          match_count += 1
          # Play a single one-sided match (no color swapping)
          print('Match ' + str(match_count) + '/' + str(match_total))
          grs += self.play_match(p1, p2, match_length, False)
    total_time = time.time() - start_time
    print('Total time for tournament: ' + str(total_time))
    self.game_results = grs
    return grs

  def export_game_data(self) -> str:
    winning_players = []
    winning_colors = []
    reasons = []
    moves = []
    times = []
    pgns = []
    whites = []
    blacks = []

    # Unzip array of game objects into arrays
    for gr in self.game_results:
      winning_players.append(gr.winning_player)
      winning_colors.append(gr.winning_color)
      reasons.append(gr.end_reason)
      moves.append(gr.moves)
      times.append(gr.time)
      pgns.append(gr.pgn)
      whites.append(gr.white_player)
      blacks.append(gr.black_player)

    # Settingup data in dict
    game_data = {
      'Winning Player': winning_players,
      'Winning Color': winning_colors,
      'End Reason': reasons,
      'Moves': moves,
      'Time': times,
      'PGN': pgns,
      'White': whites,
      'Black': blacks
    }

    df = pd.DataFrame(game_data)
    cwd = os.getcwd()
    print(cwd)
    print("HELLO")
    df.to_csv('game_output.csv', encoding='utf-8-sig')

    # files.download('output.csv')

  # exports player data
  def export_player_data(self):
    # player data
    names = []
    elos = []
    wins = []
    losses = []
    draws = []

    for player in self.players:
      names.append(player.friendly_name)
      elos.append(player.elo)
      wins.append(player.wins)
      losses.append(player.losses)
      draws.append(player.draws)

    player_data = {
      'Name': names,
      'Elo': elos,
      'Wins': wins,
      'Losses': losses,
      'Draws': draws,
    }

    df2 = pd.DataFrame(player_data)
    df2.to_csv('player_output.csv', encoding='utf-8-sig')

