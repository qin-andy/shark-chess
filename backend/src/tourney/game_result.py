import chess
import chess.pgn
from tourney.player import Player


class GameResult:
  def __init__(self):
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

  def update(self, wp: Player, bp: Player,
             board: chess.Board, game: chess.pgn.Game):
    # Basic Naming
    self.white_player = str(wp)
    self.black_player = str(bp)
    self.moves = board.fullmove_number

    game.headers['Event'] = "Bot Match"
    game.headers['White'] = str(wp)
    game.headers['Black'] = str(bp)

    # TODO : configuration options for exporting comments and headers?
    exporter = chess.pgn.StringExporter(headers=False, variations=False, comments=False)
    pgn_string = game.accept(exporter)

    # self.pgn = str(game) # pgn w/ comments, headers, etc
    self.pgn = pgn_string # pgn w/ no extras
    self.ending_fen = board.fen()

    # TODO : For testing whiel auditting, remove later
    self.pc_board = board
    self.pc_game = game

    # Matchup id (w[id],b[id])
    self.matchup_id = str(wp.id) + ',' + str(bp.id)

    # Outcome logic
    outcome = board.outcome()
    # No board outcome means turn limit was hit
    if outcome is None:
      self.winning_color = 'None'
      self.winning_player = 'None'
      self.end_reason = 'Turn Limit'
      self.r = 0.5 # TODO : double check this. should elo be calculated for turn draws?

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
          self.winning_color = 'white' # TODO : could make these bools for efficiency. 
          self.r = 1
        else:
          self.winning_player = str(bp)
          self.winning_color = 'black'
          self.r = 0
    return self

  def __str__(self):
    result = ""
    result += self.white_player + " vs " + self.black_player
    return result
