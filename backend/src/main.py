from bots.bot_manager import BotManager
from bots.composite_bots import *
from bots.simple_bots import *
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

  players_2 = [player_sk, player_ar, ]

  # gr = play_game(player_sk, player_pacifist, 300)
  # play_match(player_pacifist, player_sk, 5, True)
  tourney = Tourney('Change', 15)
  tourney.play_tournament(players_2)
  tourney.export_games_json('change')
  tourney.export_players_json('change')
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


# Tourney Steps:
  # 1. Run tourney exported jsons
  # 2. import json to reconstruct tourney, dump into mongodb
  # 3. Get tourney frommongodb, reconstruct tourney, continue tourney, export as json, put back into mongodb

# Constants for tourney-ing
MATCH_LENGTH = 50
TOURNEY_NAME = 'Continuer'
TOURNEY_PREFIX = 'continuer'
UI_PATH = '../ui/public/results/continuer/'
  
# 1. Run tourney exported jsons
def dao_cont_1():
  bot_ar = AlwaysRandomBot()
  bot_sk = SuicideKingBot()

  player_ar = Player(bot_ar, "Random")
  player_sk = Player(bot_sk, "Suicide King")
  players_2 = [player_sk, player_ar]

  tourney = Tourney(TOURNEY_NAME, MATCH_LENGTH)
  tourney.play_tournament(players_2)
  tourney.export_games_json(TOURNEY_PREFIX)
  tourney.export_players_json(TOURNEY_PREFIX)

# 2. import json to reconstruct tourney, dump into mongodb
def dao_cont_2():
  tourney = Tourney(TOURNEY_NAME, MATCH_LENGTH)
  tourney.import_games_json(TOURNEY_PREFIX + '_games.json')
  tourney.import_players_json(TOURNEY_PREFIX + '_players.json')
  tourney.engine.close()

  dao = RecordsDao()
  dao.store_tourney(tourney)

# 3. Get tourney frommongodb, reconstruct tourney, continue tourney, export as json, put back into mongodb
def dao_cont_3():
  dao = RecordsDao()
  dao_tourney = dao.get_tourney(TOURNEY_NAME)


  # For reference:
    # bot_dict["Random"] = bot_ar
    # bot_dict["Suicide King"] = bot_sk
    # bot_dict["Pacifist"] = bot_pacifist
    # bot_dict["Berserk"] = bot_berserk
    # bot_dict["Panicfish"] = bot_panic
    # bot_dict["Stockfish 100"] = bot_sf
    # bot_dict["Stockfish 5"] = bot_sf_5
    # bot_dict["Stockfish 10"] = bot_sf_10
    # bot_dict["Stockfish 20"] = bot_sf_20
  
  bot_dict = dao_tourney.get_bot_dict()
  new_player_name = 'Pacifist'
  new_player = Player(bot_dict[new_player_name], new_player_name)

  dao_tourney.continue_tourney(new_player)

  dao.store_tourney(dao_tourney) # wasteful, rewrites all games. in the future, use limited write.
  
  dao_tourney.engine.close()
  dao_tourney.export_games_json(UI_PATH + '/' + TOURNEY_PREFIX)
  dao_tourney.export_players_json(UI_PATH + '/' + TOURNEY_PREFIX)

# resets all dao_cont things
def dao_cont_cleanup():
  dao = RecordsDao()
  tourney = Tourney(TOURNEY_NAME, MATCH_LENGTH)
  dao.store_tourney(tourney)

def bot_manager_export_test():
  bm = BotManager()
  
  # List all codes
  print(list(bm.simple_bots_map.keys()))
  print(bm.composite_bot_codes)

  # Testing get simple bots
  bm.get_bot('AR')
  player_ar = Player(bm.get_bot('AR'), "Random")
  player_sk = Player(bm.get_bot('SK'), "Suicide King")
  player_pacifist = Player(bm.get_bot('PC'), "Pacifist")
  player_berserk = Player(bm.get_bot('BRK'), "Berserk")
  player_panic = Player(bm.get_bot('PF'), "Panicfish")
  player_sf = Player(bm.get_bot('SF'), 'Stockfish100')

  # simple bots playerlist
  players_simple = [player_sf, player_ar, player_pacifist]

  # constructing composite bots manually
  bot_sf_5 = WaterBot(bm.get_bot('SF'), bm.get_bot('AR'), 0.05)
  bot_sf_10 = WaterBot(bm.get_bot('SF'), bm.get_bot('AR'), 0.1)
  bot_sf_20 = WaterBot(bm.get_bot('SF'), bm.get_bot('AR'), 0.2)
  bot_shark_0_3 = SharkFishBot(bm.get_bot('AR'), 0, 3, bm.engine, bm.base_limit)

  bot_sf_sk = WaterBot(bm.get_bot('SF'), bm.get_bot('SK'), 0.5)
  bot_sf_dk = WaterBot(bm.get_bot('SF'), bm.get_bot('DK'), 0.5)
  bot_sf_brk = WaterBot(bm.get_bot('SF'), bm.get_bot('BRK'), 0.5)

  bot_sf_dc_sk_brk = WaterBot(bot_sf_brk, bot_sf_dk, 0.5)

  player_sf_5 = Player(bot_sf_5, "Stockfish 5")
  player_sf_10 = Player(bot_sf_10, "Stockfish 10")
  player_shark = Player(bot_shark_0_3, "Shark 0-3")

  player_sf_sk = Player(bot_sf_sk, "SF SK 50")
  player_sf_dk = Player(bot_sf_dk, "SF DK 50")
  player_sf_brk = Player(bot_sf_brk, "SF BRK 50")
  player_sf_lotto = Player(bot_sf_dc_sk_brk, "Lotto")
  

  players_composite_basic = [player_sf_5, player_sf_10, player_shark]
  players_composite_nested = [player_sf_sk, player_sf_dk, player_sf_brk, player_sf_lotto]

  ui_path_manager = '../ui/public/results/manager'

  tourney = Tourney('manager', 1)
  # tourney.play_tournament(players_composite_nested)
  tourney.add_players_quiet(players_simple)

  tourney.continue_tourney_multi(players_composite_basic)
  tourney.export_games_json(ui_path_manager + '/' + 'manager')
  tourney.export_players_json(ui_path_manager + '/' + 'manager')

  bm.engine.close()

if __name__ == '__main__':
  # run_tourney_export_json_test()
  # continue_tourney_json_test()
  # dao_put_tourney_test()
  # dao_read_tourney_test()
  # play_tourney()

  # dao_cont_1()
  # dao_cont_2()
  # dao_cont_3()
  # dao_cont_cleanup()

  bot_manager_export_test()




