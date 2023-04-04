from bots.bot_manager import BotManager
from bots.composite_bots import *
from bots.simple_bots import *
from tourney.tourney import *
from db.dao import *
import os

import chess
import chess.engine

# Dao Test Tourney Steps:
  # 1. Run tourney and export jsons
  # 2. import json to reconstruct tourney, export tourney to DB via dao
  # 3. import tourney from DB via dao, continue tourney, export as json for frontend AND export to db
# Goals:
  # Test tourney playing and player/game result generation
  # Test Tourney JSON import/export
  # Test Dao DB import/export
  
# Constants for tourney-ing
MATCH_LENGTH = 3
TOURNEY_NAME = 'continuer'
UI_PATH = '../ui/public/results/continuer/'
  
# 1. Run tourney and export to json
def dao_cont_1(dao: RecordsDao, bm: BotManager):
  player_ar = Player(bm.get_bot('AR'), "Random")
  player_sk = Player(bm.get_bot('SK'), "Suicide King")
  player_pc = Player(bm.get_bot('PC'), "Pacifist")
  players_2 = [player_sk, player_ar, player_pc]

  tourney = Tourney(TOURNEY_NAME, MATCH_LENGTH, bm)
  tourney.play_tournament(players_2)
  tourney.export_games_json()
  tourney.export_players_json()

# 2. import json to reconstruct tourney, dump into mongodb
def dao_cont_2(dao: RecordsDao, bm: BotManager):
  tourney = Tourney(TOURNEY_NAME, MATCH_LENGTH, bm)
  tourney.import_games_json(TOURNEY_NAME + '_games.json')
  tourney.import_players_json(TOURNEY_NAME + '_players.json')

  dao.store_tourney(tourney)

# 3. Get tourney frommongodb, reconstruct tourney, continue tourney, export as json, put back into mongodb
def dao_cont_3(dao: RecordsDao, bm: BotManager):
  dao_tourney = dao.get_tourney(TOURNEY_NAME)  
  new_player_brk = Player(bm.get_bot('BRK'), "Berserk")

  dao_tourney.continue_tourney(new_player_brk)

  dao.store_tourney(dao_tourney) # wasteful, rewrites all games. in the future, use limited write.
  
  dao_tourney.export_games_json(UI_PATH + '/' + TOURNEY_NAME)
  dao_tourney.export_players_json(UI_PATH + '/' + TOURNEY_NAME)

# resets all dao_cont things
def dao_cont_cleanup(dao: RecordsDao):
  dao.clear_tourney(TOURNEY_NAME)
  

def quiet_continue_stanard_test():
  bm = BotManager()
  
  # List all codes
  print(list(bm.simple_bots_map.keys()))
  print(bm.composite_bot_codes)

  player_ar = Player(bm.get_bot('AR'), "Random")
  player_sk = Player(bm.get_bot('SK'), "Suicide King")
  player_pc = Player(bm.get_bot('PC'), "Pacifist")
  player_brk = Player(bm.get_bot('BRK'), "Berserk")
  player_pf = Player(bm.get_bot('PF'), "Panicfish")
  player_dk = Player(bm.get_bot('DK'), 'Dance King')
  player_sf = Player(bm.get_bot('SF'), 'Stockfish100')

  bot_sf_5 = WaterBot(bm.get_bot('SF'), bm.get_bot('AR'), 0.05)
  bot_sf_10 = WaterBot(bm.get_bot('SF'), bm.get_bot('AR'), 0.1)
  bot_sf_30 = WaterBot(bm.get_bot('SF'), bm.get_bot('AR'), 0.3)
  bot_sf_50 = WaterBot(bm.get_bot('SF'), bm.get_bot('AR'), 0.5)
  bot_sf_70 = WaterBot(bm.get_bot('SF'), bm.get_bot('AR'), 0.7)
  bot_sf_75 = WaterBot(bm.get_bot('SF'), bm.get_bot('AR'), 0.75)
  bot_sf_80 = WaterBot(bm.get_bot('SF'), bm.get_bot('AR'), 0.78)
  bot_sf_90 = WaterBot(bm.get_bot('SF'), bm.get_bot('AR'), 0.9)
  bot_sf_95 = WaterBot(bm.get_bot('SF'), bm.get_bot('AR'), 0.95)


  player_sf_5 = Player(bot_sf_5, "Stockfish 5")
  player_sf_10 = Player(bot_sf_10, "Stockfish 10")
  player_sf_30 = Player(bot_sf_30, "Stockfish 30")
  player_sf_50 = Player(bot_sf_50, "Stockfish 50")
  player_sf_70 = Player(bot_sf_70, "Stockfish 70")
  player_sf_75 = Player(bot_sf_75, "Stockfish 75")
  player_sf_80 = Player(bot_sf_80, "Stockfish 80")
  player_sf_90 = Player(bot_sf_90, "Stockfish 90")
  player_sf_95 = Player(bot_sf_95, "Stockfish 95")

  lineup_standard = [
    player_ar,
    player_pc,
    player_brk,
    player_sk,
    player_dk,

    # player_sf_5,
    # player_sf_10, 
    # player_sf_30, 
    # player_sf_50, 
    # player_sf_70, 
    # player_sf_75, 
    # player_sf_80,
    # player_sf_90, 
    # player_sf_95, 
    # player_sf
  ]

  # quiet players not hving explicit games played

  # experiment players:
  bot_sf_sk = WaterBot(bm.get_bot('SF'), bm.get_bot('SK'), 0.7)
  bot_sf_dk = WaterBot(bm.get_bot('SF'), bm.get_bot('DK'), 0.7)
  bot_sf_brk = WaterBot(bm.get_bot('SF'), bm.get_bot('BRK'), 0.7)
  bot_sf_dc_sk_brk = WaterBot(bot_sf_brk, bot_sf_dk, 0.5)

  player_sf_sk = Player(bot_sf_sk, "SF SK 50")
  player_sf_dk = Player(bot_sf_dk, "SF DK 50")
  player_sf_brk = Player(bot_sf_brk, "SF BRK 50")
  player_sf_lotto = Player(bot_sf_dc_sk_brk, "Lotto")

  player_sns = Player(bm.get_bot('SNS'), 'Sensitive')

  lineup_performing = [
    # player_sf_sk,
    # player_sf_dk, 
    # player_sf_brk, 
    # player_sf_lotto, 
    player_sns
  ]

  ui_path_manager = '../ui/public/results/manager'


  # standard lineup is added quietly
  tourney = Tourney('manager', 10, bm)
  tourney.add_players_quiet(lineup_standard)

  tourney.continue_tourney_multi(lineup_performing)
  tourney.export_games_json(ui_path_manager + '/' + 'manager')
  tourney.export_players_json(ui_path_manager + '/' + 'manager')

  bm.engine.close()


def bot_manager_export_test():
  
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

  # quiet players not hving explicit games played

  ui_path_manager = '../ui/public/results/manager'

  tourney = Tourney('manager', 10, bm)
  tourney.play_tournament(players_composite_nested)
  tourney.add_players_quiet(players_simple )

  tourney.continue_tourney_multi(players_composite_basic)
  tourney.export_games_json(ui_path_manager + '/' + 'manager')
  tourney.export_players_json(ui_path_manager + '/' + 'manager')

if __name__ == '__main__':
  bm = BotManager()
  dao = RecordsDao(bm)

  dao_cont_1(dao, bm)
  dao_cont_2(dao, bm)
  dao_cont_3(dao, bm)
  # dao_cont_cleanup(dao)

  bm.engine.close()
  dao.client.close()

  # bot_manager_export_test()
  # quiet_continue_stanard_test()




