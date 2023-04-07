import json
import time

import chess
import chess.pgn
import chess.engine
import os
from bots.bot_manager import BotManager
from bots.composite_bots import WaterBot

from bots.simple_bots import *
from tourney.elo import calculate_elos
from tourney.game_result import GameResult
from tourney.player import Player


class Tourney:
  def __init__(self, friendly_name: str, match_length: int, bot_manager: BotManager = None):
    """
    Creates a tourney. Need to pass in name, match length, and bot manager.
    """
    if bot_manager == None:  # This case in unideal because the engine is more difficult to close
      bot_manager = BotManager()

    # Tourney settingstou
    self.match_length = match_length
    self.elo_k = 32  # controls Elo gain/loss

    self.game_results: list[GameResult] = []
    self.players: list[Player] = []
    self.friendly_name = friendly_name

    self.game_number = 0  # increment after a game result is assigend this. pseudo id

    self.bot_manager = bot_manager

  def play_game(self, wp: Player, bp: Player, turn_limit: int) -> GameResult:
    """
    Play a single game between two players, repeatedly calling each player's move method.
    At the turn limit, the result of the ame will be a draw.
    Creates a GameResult object to store game level info.
    """
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
      if comment != '':  # empty comments mean no comment (!)
        node.comment = comment
      board.push(move)
      turns += 1
    game.end()
    game_result = GameResult()
    game_result.from_chess(wp, bp, board, game)

    # set ID. setting it externally here cuz its tourney_level, even if its stored on GR level.
    # TODO : necessary?
    game_result.game_number = self.game_number
    self.game_number += 1

    game_result.time = time.time() - start_time
    return game_result

  def update_player_data(self, wp: Player, bp: Player, gr: GameResult) -> None:
    """
    Updates player level statistics based on GameResult.
    Usually called right after a game is played.
    """
    # Updates player ELO, wins, losses, draws after result

    d = 0  # default
    if gr.winning_color == 'white':
      d = 1  # for elo calc
      wp.wins += 1
      bp.losses += 1
    elif gr.winning_color == 'black':
      d = 0  # for elo calc
      wp.losses += 1
      bp.wins += 1
    else:  # draw case
      d = 0.5
      bp.draws += 1
      wp.draws += 1

    wp.elo, bp.elo = calculate_elos(wp.elo, bp.elo, self.elo_k, d)
    # print(str(wp) + ': ' + str(wp.elo) + ', ' + str(bp) + ': ' + str(bp.elo))

  def play_match(self, p1: Player, p2: Player, count, swap_colors=False) -> list[GameResult]:
    """
    Helper to play multiple games between two players.
    Repeatedly calls the play_game method.
    Returns a list of the game results, and updates player level statistics.
    """
    print('=========<' + str(p1) + ' [vs] ' + str(p2) + '>=========')

    # Time and play games
    start_time = time.time()
    grs = []  # game results array

    for i in range(count):
      print('Game [' + str(i + 1) + '/' + str(count) +
            "] of [" + str(p1) + "] vs [" + str(p2) + "]")
      gr = self.play_game(p1, p2, 300)
      print(gr.winning_player +
            ' wins in [' + str(gr.moves) + '] turns in [' + str(gr.time) + '] seconds')
      self.update_player_data(p1, p2, gr)
      grs.append(gr)

    if swap_colors:  # TODO: Recursive case, could be cleaner
      grs2 = self.play_match(p2, p1, count, False)
      grs += grs2

    print('Total Time: ' + str(time.time() - start_time))
    print()

    return grs

  def play_tournament(self, players: list[Player]) -> list[GameResult]:
    """
    Plays a round robin tourney with the given list of players.
    I.e. plays a match of the specified length between all players.
    Skips mirror matches.
    Players are assigned ids and statistics are updated by the end of the tourney.
    Game results are stored as a field and also returned.
    """
    self.players = players
    # build player ids
    counter = 0
    for player in self.players:
      player.id = counter
      counter += 1

    match_length = self.match_length

    start_time = time.time()
    match_total = (len(players) ** 2) - len(players)
    match_count = 0
    grs = []
    for p1 in players:
      for p2 in players:
        if str(p1) != str(p2):  # skip self play matches
          match_count += 1
          # Play a single one-sided match (no color swapping)
          print('Match ' + str(match_count) + '/' + str(match_total))
          grs += self.play_match(p1, p2, match_length, False)
    total_time = time.time() - start_time
    print('Total time for tournament: ' + str(total_time))
    self.game_results = grs
    return grs

  def add_players_quiet(self, players: list[Player]):
    """
    Add players quietly to a tourney, without playing any games with them.
    Assigns player ids.
    """
    for player in players:
      player.id = len(self.players)
      self.players.append(player)

  def continue_tourney(self, new_player: Player) -> list[GameResult]:
    """
    Adds a new player to the tourney and runs a match with every existing player.
    Mutates the player object.
    Returns the new player and new game results
    """
    match_count = 0
    match_total = len(self.players)
    new_player.id = len(self.players)  # assign new player the appropriate id

    grs = self.game_results
    new_grs = []  # used to calculate the diffs
    start_time = time.time()

    # new player as white
    # note the loose convention of match orders being all white then all black plays is brokn here
    for old_player in self.players:
      match_count += 1

      print('Match ' + str(match_count) + '/' + str(match_total))
      # TODO : should validate previous results and new match length are same.
      new_grs += self.play_match(new_player, old_player,
                                 self.match_length, False)
      # Note : playing continued games out of order here.
      new_grs += self.play_match(old_player, new_player,
                                 self.match_length, False)

    grs += new_grs
    total_time = time.time() - start_time

    # have this at the end, bc we iterate through players above
    self.players.append(new_player)

    print('Total time for continution: ' + str(total_time))
    return new_grs  # used in dao

  def continue_tourney_multi(self, new_players: list[Player]):
    """
    Continues tourney with a list of players.
    """
    new_grs = []
    for new_player in new_players:
      # a is discarded
      new_gr = self.continue_tourney(new_player)
      new_grs.append(new_gr)

    # original players list will be mutated
    return new_grs

  def export_games_json(self, file_prefix=None) -> str:
    """
    Exports stored games data as json named <file_prefix>_games.json.
    Defaults file prefix to the tourney's friendly name.
    """
    if file_prefix == None:
      file_prefix = self.friendly_name
    data = []
    for gr in self.game_results:
      data.append(gr.to_dict())

    json_data = json.dumps(data, indent=2)
    with open(file_prefix + '_games.json', 'w') as file:
      file.write(json_data,)

  def export_players_json(self, file_prefix=None):
    """
    Exports stored player data as json named <file_prefix>_players.json.
    Defaults file prefix to the tourney's friendly name.
    """
    if file_prefix == None:
      file_prefix = self.friendly_name
    data = []
    for player in self.players:
      data.append(player.to_dict())

    json_data = json.dumps(data, indent=2)

    with open(file_prefix + '_players.json', 'w') as file:
      file.write(json_data,)

  def get_tourney_settings(self) -> dict:
    """
    Gets tourney level settings information as a dict.
    Match length, name.
    """
    settings = {
        'Name': self.friendly_name,
        'Match Length': self.match_length,
    }
    return settings

  def export_tourney_json(self, file_prefix=None):
    """
    Exports games, players, tourney settings as json <file_name>_tourney.json
    """
    if file_prefix == None:
      file_prefix = self.friendly_name

    player_data = []
    for player in self.players:
      player_data.append(player.to_dict())

    game_data = []
    for gr in self.game_results:
      game_data.append(gr.to_dict())

    tourney_dict = {
        'Games': game_data,
        'Players': player_data,
        'Settings': self.get_tourney_settings()
    }

    with open(file_prefix + '_tourney.json', 'w') as file:
      file.write(json.dumps(tourney_dict, indent=2),)

  def import_games_json(self, file_name):
    """
    Import game results and updates tourney fields.
    Parameter requires file extension.
    """
    path = '../../' + file_name  # TODO : refactor
    dirname = os.path.dirname(__file__)
    filename = os.path.join(dirname, path)
    g_file = open(filename)
    g_jdata = json.loads(g_file.read())

    game_results = []
    for game_dict in g_jdata:
      gr = GameResult()
      gr.from_dict(game_dict)
      game_results.append(gr)
    self.game_results = game_results

  def import_players_json(self, file_name):
    """
    Import players and updates tourney fields.
    Parameter requires file extension.
    """
    path = '../../' + file_name  # TODO : refactor
    dirname = os.path.dirname(__file__)
    filename = os.path.join(dirname, path)
    p_file = open(filename)
    p_jdata = json.loads(p_file.read())

    # Convert list of dicts into list of player objects
    players = []
    for player_dict in p_jdata:
      name = player_dict['Name']
      bot = self.bot_manager.get_bot(player_dict['Bot Settings'])
      player = Player(name, bot)
      player.from_dict(player_dict)
      players.append(player)

  def import_tourney_json(self, file_name):
    """
    Import tourney games and players and updates tourney fields.
    Parameter requires file extension.
    """
    path = '../../' + file_name  # TODO : refactor
    dirname = os.path.dirname(__file__)
    filename = os.path.join(dirname, path)
    t_file = open(filename)
    t_data = json.loads(t_file.read())

    # Todo: add validation here
    g_data = t_data['Games']
    p_data = t_data['Players']

    game_results = []
    for game_dict in g_data:
      gr = GameResult()
      gr.from_dict(game_dict)
      game_results.append(gr)
    self.game_results = game_results

    players = []
    for player_dict in p_data:
      name = player_dict['Name']
      bot = self.bot_manager.get_bot(player_dict['Bot Settings'])
      player = Player(name, bot)
      player.from_dict(player_dict)
      players.append(player)
    self.players = players
