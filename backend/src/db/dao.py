from pymongo import MongoClient
import os
import json

from tourney.tourney import *

DB_NAME = 'shark-chess'

class RecordsDao:
  """
  Data access object to interface with DB, storing and constructing tourneys
  """

  # TODO: see if we can refactor this somehow. bot amanager is used in a lot of different places.
  def __init__(self, bot_manager: BotManager) -> None:
    """
    Requires a bot manager, used for constructing bots for importing tourney players
    """
    self.bot_manager = bot_manager
    self.client = MongoClient('localhost', 27017)
    self.db = self.client[DB_NAME]
    print('Initializing RecordsDao for ' + DB_NAME)

  def store_tourney(self, tourney: Tourney):
    """
    Stores a tourney and its results in the db.
    Wipes previous instances of the tourney.
    Tourney prefix is determined by tourney name.
    The collections generated in DB are:
      * <name>_games - stores the game results
      * <name>_players - stores the
      * <name>_tourney_settings
    """
    name = tourney.friendly_name
    db = self.db

    games = [game.to_dict() for game in tourney.game_results]
    players = [player.to_dict() for player in tourney.players]
    settings = tourney.get_tourney_settings()

    # Clears previous existing data
    deleted = self.clear_tourney(name)
    print('Deleted games: ' + str(deleted))

    db[name + '_games'].insert_many(games)
    db[name + '_players'].insert_many(players)

    db[name + '_tourney_settings'].insert_one(settings)

  def clear_tourney(self, name: str):
    """
    Deletes all records of a tourney (all prefixed collections).
    Returns number of deleted games.
    """
    db = self.db
    count = 0  # count deleted records
    count += db[name + '_games'].delete_many({}).deleted_count
    db[name + '_players'].delete_many({})
    db[name + '_tourney_settings'].delete_many({})
    return count

  def get_tourney_as_dict(self, name) -> dict:
    """
    Gets tourney as a dictionary (games, players, and tourney level settings)
    """
    db = self.db
    if (name + '_tourney_settings') not in db.list_collection_names():
      print('Tourney not found!')  # TODO : Error handle this
      return None

    games = db[name + '_games'].find()
    players = db[name + '_players'].find()
    settings = db[name + '_tourney_settings'].find_one()

    tourney_dict = {
        'Games': list(games),
        'Players': list(players),
        'Settings': settings
    }
    return tourney_dict

  def get_tourney(self, name: str, gameless=False) -> Tourney:
    """
    Retrieves and constructs a tourney object by its name (prefixed collections in DB)
    """
    tourney_dict = self.get_tourney_as_dict(name)
    games = tourney_dict['Games']
    players = tourney_dict['Players']
    settings = tourney_dict['Settings']
    tourney = Tourney(name, settings['Match Length'], self.bot_manager)
    if not gameless:  # for tourney continuation, previous games aren't important
      for game in games:
        gr = GameResult()
        gr.from_dict(game)
        tourney.game_results.append(gr)

    new_players: list[Player] = []
    for player in players:
      player_name = player['Name']
      bot = self.bot_manager.get_bot(player['Bot Settings'])
      new_player = Player(player_name, bot)
      new_player.from_dict(player)
      new_players.append(new_player)
    tourney.add_players_quiet(new_players)
    return tourney

  def add_to_tourney(self, name, new_games, new_players):
    """
    Appends new games/players to a tourney collection.
    Used for storing results from a tourney continuation.
    Warning: there's no validation here for this function. Be careful!!!!!
    """
    db = self.db
    if (name + '_tourney_settings') not in db.list_collection_names():
      print('Tourney not found!')  # TODO : Error handle this
      return None

    games = db[name + '_games']
    players = db[name + '_players']

    games.insert_many(new_games)
    players.insert_many(new_players)
