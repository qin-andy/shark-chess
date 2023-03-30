from pymongo import MongoClient
import os
import json

from tourney.tourney import *

# Constants
DB_NAME = 'shark-chess'
class RecordsDao:
  def __init__(self) -> None:
    self.client = MongoClient('localhost', 27017)
    self.db = self.client[DB_NAME]
    print('Initializing RecordsDao for ' + DB_NAME)

  # Stores a tourney and its results in the db
  # Wipes previous instances of the tourney. 
  def store_tourney(self, tourney: Tourney):
    name = tourney.friendly_name
    db = self.db
    
    games = [game.to_dict() for game in tourney.game_results]
    players = [player.to_dict() for player in tourney.players]

    # Clears previous existing data
    db[name+'_games'].delete_many({})
    db[name+'_players'].delete_many({})
    db[name+'_tourney_settings'].delete_many({})

    db[name+'_games'].insert_many(games)
    db[name+'_players'].insert_many(players)

    # {
    #   'Name': self.friendly_name,
    #   'Match Length': self.match_length,
    #   'Players': player_data,
    #   'Games': game_data
    # }
    db[name+'_tourney_settings'].insert_one({
        'Name': name,
        'Match Length': tourney.match_length,
    })


  # Retrieves and constructs tourney object by name
  def get_tourney(self, name, gameless=False):
    db = self.db
    if (name + '_tourney_settings') not in db.list_collection_names():
      print('Tourney not found!') # TODO : Error handle this
      return None
    
    games = db[name+'_games'].find()
    players = db[name+'_players'].find()
    settings = db[name+'_tourney_settings'].find_one()

    tourney = Tourney(name, settings['Match Length'])
    if not gameless: # for tourney continuation, previous games aren't important
      for game in games:
        gr = GameResult()
        gr.from_dict(game)
        tourney.game_results.append(gr)
    
    bot_dict = tourney.get_bot_dict()
    for player in players:
      player_name = player['Name']
      bot = bot_dict[player_name]
      new_player = Player(bot, player_name)
      new_player.from_dict(player)
      tourney.players.append(new_player)
    return tourney
  
  # Warning: there's no validation here for this function. Be careful!!!!!
  def add_to_tourney(self, name, new_games, new_players):
    db = self.db
    if (name + '_tourney_settings') not in db.list_collection_names():
      print('Tourney not found!') # TODO : Error handle this
      return None
    
    games = db[name+'_games']
    players = db[name+'_players']

    games.insert_many(new_games)
    players.insert_many(new_players)
  
  