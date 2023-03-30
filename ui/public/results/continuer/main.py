from bots.bots import *
from tourney.tourney import *
from db.dao import *
import os
import chess
import chess.engine


ENGINE_PATH = '../stockfish/stockfish-ubuntu-20.04-x86-64'

def run_tourney_export_json_test():
  bot_ar = AlwaysRandomBot()
  bot_sk = SuicideKingBot()
  bot_pacifist = PacifistBot()
  bot_berserk = BerserkBot()

  # Stockfish Bots\

  # Configuring path
  # Rememeber to install stockfish in the project root and chmod 755 (?) /to allow permissions
  stockfish_path = ENGINE_PATH
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

  players_2 = [player_sk, player_ar]

  # gr = play_game(player_sk, player_pacifist, 300)
  # play_match(player_pacifist, player_sk, 5, True)
  tourney = Tourney('Continuer', 15)
  tourney.play_tournament(players_2)
  tourney.export_games_json('continue')
  tourney.export_players_json('continue')
  engine.close()

def continue_tourney_json_test():
  bot_ar = AlwaysRandomBot()
  stockfish_path = ENGINE_PATH
  dirname = os.path.dirname(__file__)
  filename = os.path.join(dirname, stockfish_path)
  engine = chess.engine.SimpleEngine.popen_uci(filename)
  base_limit = chess.engine.Limit(time=0.1, depth=5)

  bot_sf = Stockfish100Bot(engine, base_limit)
  bot_sf_5 = WaterBot(bot_sf, bot_ar, 0.05)
  player_sf_5 = Player(bot_sf_5, "ADDED")

  tourney = Tourney('Import Test', 3)
  tourney.engine = engine
  tourney.import_games_json('new_dict_games.json')
  tourney.import_players_json('new_dict_players.json')

  tourney.continue_tourney(player_sf_5)

  tourney.export_games_json('newnew_dict')
  tourney.export_players_json('newnew_dict')
  engine.close()


def dao_put_tourney_test():
  # Import dao
  tourney = Tourney('imported', 3)
  tourney.import_games_json('dao3_games.json')
  tourney.import_players_json('dao3_players.json')
  tourney.engine.close()

  dao = RecordsDao()
  dao.store_tourney(tourney)


def dao_read_tourney_test():
  dao = RecordsDao()
  dao_tourney = dao.get_tourney('imported')
  dao_tourney.engine.close()
  dao_tourney.export_games_json('dao3_retrieved')
  dao_tourney.export_players_json('dao3_retrieved')


def dao_continue_tourney_test():
  dao = RecordsDao()



if __name__ == '__main__':
  run_tourney_export_json_test()
  # continue_tourney_json_test()
  # dao_put_tourney_test()
  # dao_read_tourney_test()
  # play_tourney()


