
from bots.bots import ChessBot
import time


class Player:
  def __init__(self, bot: ChessBot, friendly_name):
    self.id: int = None # Assigned at tourney level (At start tourney)
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
    start_time = time.time()
    move = self.bot.make_move(board)
    self.total_thinking_time += time.time() - start_time
    self.total_moves += 1
    return move
  
  # Exports player as a dictionary
  def to_dict(self):
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
    return player_dict
  
  # updates fields based on player dictionary
  def from_dict(self, player_dict):
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