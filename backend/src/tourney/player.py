
from bots.chess_bot import ChessBot
import time


class Player:
  """
  Represents a player in a tourney.
  Holds bot for move generation.
  Also holds a friendly display name and player-level statistics.
  Has an ID controlled at tourney level.
  """

  def __init__(self, friendly_name, bot: ChessBot):
    self.id: int = None  # Assigned at tourney level (At start tourney)
    self.friendly_name: str = friendly_name
    self.bot: ChessBot = bot
    self.elo: int = 800  # default Elo
    self.wins: int = 0
    self.losses: int = 0
    self.draws: int = 0

    # Game to game stats
    self.total_thinking_time: float = 0
    self.total_moves: int = 0

  def move(self, board):
    """
    Calls the inner bot to make a move. Includes timing logic. 
    """
    start_time = time.time()
    move = self.bot.make_move(board)
    self.total_thinking_time += time.time() - start_time
    self.total_moves += 1
    return move

  def to_dict(self):
    """
    Exports player information as a dictionary for serialization/storage
    """

    # {
    #   "Name": "Random",
    #   "ID": 1,
    #   "Elo": 824,
    #   "Wins": 5,
    #   "Losses": 2,
    #   "Draws": 11,
    #   "Think Time": 0.2440176010131836,
    #   "Moves": 2092
    # },

    player_dict = {}
    player_dict['Name'] = self.friendly_name
    player_dict['ID'] = self.id
    player_dict['Elo'] = self.elo
    player_dict['Wins'] = self.wins
    player_dict['Losses'] = self.losses
    player_dict['Draws'] = self.draws
    player_dict['Think Time'] = self.total_thinking_time
    player_dict['Moves'] = self.total_moves

    player_dict['Bot Settings'] = self.bot.settings

    return player_dict

  def from_dict(self, player_dict):
    """
    Updates fields with player information from dictionary. Used for reading in data.
    Note that name and bot are not imported, but assigned in the constructor. 
    """
  
    self.name = player_dict['Name'] # might be redundant, since this is set in constructor.
    self.id = player_dict['ID']
    self.elo = int(player_dict['Elo'])
    self.wins = int(player_dict['Wins'])
    self.losses = int(player_dict['Losses'])
    self.draws = int(player_dict['Draws'])
    self.total_thinking_time = float(player_dict['Think Time'])
    self.total_moves = int(player_dict['Moves'])

    return self

  def __str__(self):
    return self.friendly_name
