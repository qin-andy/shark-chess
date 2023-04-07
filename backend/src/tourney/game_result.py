import chess
import chess.pgn
from tourney.player import Player


class GameResult:
  """
  Stores information for a concluded chess game.
  """

  def __init__(self):
    """
    Initalizes an empty GameResult with values to be set manually.
    See :func:`from_chess`
    """
    self.game_number = 0  # TODO : is this still necessary?
    self.white_player: str = None
    self.black_player: str = None
    self.winning_player = None
    self.winning_color = None
    self.r: float = None  # numerical value representing result. 1=w, 0.5=d, 0=b
    self.moves: int = None
    self.time: float = None
    self.pgn: str = None
    self.end_reason: str = None
    self.pc_game = None
    self.pc_board = None
    self.matchup_id: str = None
    self.ending_fen: str = None

  def from_chess(self, wp: Player, bp: Player,
                 board: chess.Board, game: chess.pgn.Game):
    """
    Takes information available after a game has ended and populates the relevant fields..
    """

    # Basic Naming
    self.white_player = str(wp)
    self.black_player = str(bp)
    self.moves = board.fullmove_number

    game.headers['Event'] = "Bot Match"
    game.headers['White'] = str(wp)
    game.headers['Black'] = str(bp)

    # TODO : configuration options for exporting comments and headers?
    exporter = chess.pgn.StringExporter(
        headers=False, variations=False, comments=False)
    pgn_string = game.accept(exporter)

    # self.pgn = str(game) # pgn w/ comments, headers, etc
    self.pgn = pgn_string  # pgn w/ no extras
    self.ending_fen = board.fen()

    # Matchup id (w[id],b[id])
    self.matchup_id = str(wp.id) + ',' + str(bp.id)

    # Outcome logic
    outcome = board.outcome()
    # No board outcome means turn limit was hit

    # Conditional logic for determining winner/loser and r value for ELO calculation
    if outcome is None:
      self.winning_color = 'None'
      self.winning_player = 'None'
      self.end_reason = 'Turn Limit'
      self.r = 0.5

    else:
      self.end_reason = outcome.termination.name
      if outcome.winner is None:
        # No winner means stalemate
        self.winning_color = 'None'
        self.winning_player = 'None'
        self.r = 0.5
      else:
        # Winner is either black or white bot
        if outcome.winner:
          self.winning_player = str(wp)
          self.winning_color = 'white'
          self.r = 1
        else:
          self.winning_player = str(bp)
          self.winning_color = 'black'
          self.r = 0
    return self

  def to_dict(self):
    """
    Exports relevant game result items as a dictionary. 
    """

    # """
    # game_data = {
    #   'Matchup ID': matchup_ids,
    #   'Winning Player': winning_players,
    #   'Winning Color': winning_colors,
    #   'End Reason': reasons,
    #   'Moves': moves,
    #   'Time': times,
    #   'PGN': pgns,
    #   'White': whites,
    #   'Black': blacks,
    #   'Ending FEN': ending_fens
    # }
    # """

    game_dict = {}
    game_dict['Matchup ID'] = self.matchup_id
    game_dict['Winning Player'] = self.winning_player
    game_dict['Winning Color'] = self.winning_color
    game_dict['End Reason'] = self.end_reason
    game_dict['Moves'] = self.moves
    game_dict['Time'] = self.time
    game_dict['PGN'] = self.pgn
    game_dict['White'] = self.white_player
    game_dict['Black'] = self.black_player
    game_dict['Ending FEN'] = self.ending_fen
    return game_dict

  def from_dict(self, game_dict):
    """
    Updates game result fields from a dictionary created using the `to_dict` method
    """
    self.white_player = game_dict['White']
    self.black_player = game_dict['Black']
    self.winning_player = game_dict['Winning Player']
    self.winning_color = game_dict['Winning Color']
    self.moves = game_dict['Moves']
    self.time = game_dict['Time']
    self.pgn = game_dict['PGN']
    self.end_reason = game_dict['End Reason']
    self.matchup_id = game_dict['Matchup ID']
    self.ending_fen = game_dict['Ending FEN']
    return self

  def __str__(self):
    result = ""
    result += self.white_player + " vs " + self.black_player
    return result
