from bots.bots import *
from tourney.tourney import *
import os
import chess
import chess.engine


def player_game_test():
  bot_ar = AlwaysRandomBot()
  bot_sk = SuicideKingBot()
  bot_pacifist = PacifistBot()
  bot_berserk = BerserkBot()

  # Stockfish Bots\

  # Configuring path
  # Rememeber to install stockfish in the project root and chmod 755 (?) /to allow permissions
  stockfish_path = '../stockfish/stockfish-ubuntu-20.04-x86-64'
  dirname = os.path.dirname(__file__)
  filename = os.path.join(dirname, stockfish_path)
  engine = chess.engine.SimpleEngine.popen_uci(filename)
  base_limit = chess.engine.Limit(time=0.1, depth=5)

  bot_sf = Stockfish100Bot(engine, base_limit)
  bot_sf_5 = WaterBot(bot_sf, bot_ar, 0.05)
  bot_sf_10 = WaterBot(bot_sf, bot_ar, 0.1)
  bot_sf_20 = WaterBot(bot_sf, bot_ar, 0.2)
  bot_panic = PanicFishBot(engine, base_limit)

  player_ar = Player(bot_ar, "Random")
  player_sk = Player(bot_sk, "Suicide King")
  player_pacifist = Player(bot_pacifist, "Pacifist")
  player_berserk = Player(bot_berserk, "Berserk")
  player_panic = Player(bot_panic, "Panicfish")

  player_sf = Player(bot_sf, "Stockfish 100")
  player_sf_5 = Player(bot_sf_5, "Stockfish 5")
  player_sf_10 = Player(bot_sf_10, "Stockfish 10")
  player_sf_20 = Player(bot_sf_20, "Stockfish 20")

  players_0 = [player_sk, player_ar, player_pacifist, player_sf, player_berserk,
              player_sf_5, player_sf_10, player_sf_20, player_panic]
  
  players_1 = [player_sk, player_ar, player_pacifist, player_berserk]

  # gr = play_game(player_sk, player_pacifist, 300)
  # play_match(player_pacifist, player_sk, 5, True)
  tourney = TourneyManager(3)
  tourney.play_tournament(players_1)
  tourney.export_game_data('new_dict')
  tourney.export_player_data('new_dict')
  engine.close()

def import_test():
  bot_ar = AlwaysRandomBot()
  stockfish_path = '../stockfish/stockfish-ubuntu-20.04-x86-64'
  dirname = os.path.dirname(__file__)
  filename = os.path.join(dirname, stockfish_path)
  engine = chess.engine.SimpleEngine.popen_uci(filename)
  base_limit = chess.engine.Limit(time=0.1, depth=5)

  bot_sf = Stockfish100Bot(engine, base_limit)
  bot_sf_5 = WaterBot(bot_sf, bot_ar, 0.05)
  # player_sf_5 = Player(bot_sf_5, "ADDED")

  tourney = TourneyManager(3)
  tourney.import_game_results('new_dict_games.json')
  tourney.import_player_results('new_dict_players.json')

  # tourney.continue_tourney(player_sf_5)

  tourney.export_game_data('newnew_dict')
  tourney.export_player_data('newnew_dict')



if __name__ == '__main__':
  # player_game_test()
  import_test()


