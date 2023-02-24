from bots.bots import *
from tourney.tourney import *
import os
import chess
import chess.engine


def player_game_test():
  bot_ar = AlwaysRandomBot()
  bot_sk = SuicideKingBot()
  bot_pacifist = PacifistBot()

  # Stockfish Bots\

  # Configuring path
  # Rememeber to install stockfish in the project root and chmod 755 (?) /to allow permissions
  stockfish_path = '../stockfish/stockfish-ubuntu-20.04-x86-64'
  dirname = os.path.dirname(__file__)
  filename = os.path.join(dirname, stockfish_path)
  engine = chess.engine.SimpleEngine.popen_uci(filename)
  base_limit = chess.engine.Limit(time=0.1, depth=10)

  bot_sf = Stockfish100Bot(engine, base_limit)


  player_ar = Player(bot_ar, "RandomPlayer")
  player_sk = Player(bot_sk, "SKPlayer")
  player_pacifist = Player(bot_pacifist, "PacifistPlayer")
  player_sf = Player(bot_sf, "Stockfish100")

  players = [player_sk, player_ar]
  # gr = play_game(player_sk, player_pacifist, 300)
  # play_match(player_pacifist, player_sk, 5, True)
  tourney = TourneyManager(players, 10)
  tourney.play_tournament()
  tourney.to_csv()
  engine.close()


if __name__ == '__main__':
  # play_test_game()
  # play_test_match()
  # play_test_tourney()
  player_game_test()


