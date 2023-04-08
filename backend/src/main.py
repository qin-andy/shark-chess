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
  player_ar = Player("Random", bm.get_simple_bot('AR'), )
  player_sk = Player("Suicide King", bm.get_simple_bot('SK'), )
  player_pc = Player("Pacifist", bm.get_simple_bot('PC'),)
  player_brk_m = Player('Berserk SF', BerserkModularBot(bm.get_simple_bot('SF')))


  # Nested composite
  bot_sf_dk = WaterBot(bm.get_simple_bot('SF'), bm.get_simple_bot('DK'), 0.2)
  bot_sf_brk = WaterBot(bm.get_simple_bot('SF'), bm.get_simple_bot('BRK'), 0.2)
  bot_sf_dc_sk_brk = WaterBot(bot_sf_brk, bot_sf_dk, 0.5)

  player_sf_lotto = Player("Lotto", bot_sf_dc_sk_brk)

  # Simple composite
  player_part_sk = Player("Part SK", WaterBot(
      bm.get_simple_bot('SF'), bm.get_simple_bot('SK'), 0.2))
  players_2 = [player_sk, player_ar, player_brk_m]

  tourney = Tourney(TOURNEY_NAME, MATCH_LENGTH, bm)
  tourney.play_tournament(players_2)
  tourney.export_tourney_json()

# 2. import json to reconstruct tourney, dump into mongodb
def dao_cont_2(dao: RecordsDao, bm: BotManager):
  tourney = Tourney(TOURNEY_NAME, MATCH_LENGTH, bm)
  tourney.import_tourney_json(TOURNEY_NAME + '_tourney.json')

  dao.store_tourney(tourney)

# 3. Get tourney frommongodb, reconstruct tourney, continue tourney, export as json, put back into mongodb
def dao_cont_3(dao: RecordsDao, bm: BotManager):
  dao_tourney = dao.get_tourney(TOURNEY_NAME)
  new_player_brk = Player('Berserk', bm.get_simple_bot('BRK'))

  dao_tourney.continue_tourney(new_player_brk)

  # wasteful, rewrites all games. in the future, use limited write.
  dao.store_tourney(dao_tourney)

  dao_tourney.export_tourney_json(UI_PATH + '/' + TOURNEY_NAME)

# resets all dao_cont things
def dao_cont_cleanup(dao: RecordsDao):
  dao.clear_tourney(TOURNEY_NAME)


def quiet_continue_stanard_test(bm: BotManager):

  # List all codes
  print(list(bm.simple_bots_map.keys()))
  print(bm.composite_bot_codes)

  player_ar = Player('Random', bm.get_bot('AR'))
  player_sk = Player('Suicide King', bm.get_bot('SK'))
  player_pc = Player('Pacifist', bm.get_bot('PC'))
  player_brk = Player('Berserk', bm.get_bot('BRK'))
  player_pf = Player('Panicfish', bm.get_bot('PF'))
  player_dk = Player('Danceking', bm.get_bot('DK'))
  player_sf = Player('Stockfish', bm.get_bot('SF'))

  lineup_standard = [
      player_ar,
      player_pc,
      player_brk,
      player_sk,
      player_dk,
  ]

  # quiet players not hving explicit games played

  # experiment players:
  bot_sf_sk = WaterBot(bm.get_simple_bot('SF'), bm.get_simple_bot('SK'), 0.2)
  bot_sf_dk = WaterBot(bm.get_simple_bot('SF'), bm.get_simple_bot('DK'), 0.2)
  bot_sf_brk = WaterBot(bm.get_simple_bot('SF'), bm.get_simple_bot('BRK'), 0.2)
  bot_sf_dc_sk_brk = WaterBot(bot_sf_brk, bot_sf_dk, 0.5)

  player_sf_sk = Player("Quarter Suicide", bot_sf_sk)
  player_sf_dk = Player("Quarter Dance", bot_sf_dk)
  player_sf_brk = Player("Quarter Berserk", bot_sf_brk)
  player_sf_lotto = Player("Lotto", bot_sf_dc_sk_brk)

  player_sns = Player(bm.get_simple_bot('SNS'), 'Sensitive')

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


def bot_manager_export_test(bm: BotManager):
  # List all codes
  print(list(bm.simple_bots_map.keys()))
  print(bm.composite_bot_codes)

  # Testing get simple bots
  bm.get_simple_bot('AR')

  # constructing composite bots manually

  bot_sf_sk = WaterBot(bm.get_simple_bot('SF'), bm.get_simple_bot('SK'), 0.5)
  bot_sf_dk = WaterBot(bm.get_simple_bot('SF'), bm.get_simple_bot('DK'), 0.5)
  bot_sf_brk = WaterBot(bm.get_simple_bot('SF'), bm.get_simple_bot('BRK'), 0.5)

  bot_sf_dc_sk_brk = WaterBot(bot_sf_brk, bot_sf_dk, 0.5)

  player_sf_sk = Player("Quarter Suicide", bot_sf_sk)
  player_sf_dk = Player("Quarter Dance", bot_sf_dk)
  player_sf_brk = Player("Quarter Berserk", bot_sf_brk)
  player_sf_lotto = Player("Lotto", bot_sf_dc_sk_brk)

  players_composite_nested = [player_sf_sk,
                              player_sf_dk, player_sf_brk, player_sf_lotto]

  # quiet players not hving explicit games played

  # ui_path_manager = '../ui/public/results/manager'
  ui_path_manager = '.'

  tourney = Tourney('export', 1, bm)
  tourney.play_tournament(players_composite_nested)
  # tourney.add_players_quiet(players_simple )

  # tourney.continue_tourney_multi(players_composite_basic)
  tourney.export_games_json(ui_path_manager + '/' + 'export')
  tourney.export_players_json(ui_path_manager + '/' + 'export')


def run_tourney_store_db(dao: RecordsDao, bm: BotManager):
  # List all codes
  print(list(bm.simple_bots_map.keys()))
  print(bm.composite_bot_codes)

  player_ar = Player('Random', bm.get_simple_bot('AR'))
  player_sk = Player('Suicide King', bm.get_simple_bot('SK'))
  player_pc = Player('Pacifist', bm.get_simple_bot('PC'))
  player_brk = Player('Berserk', bm.get_simple_bot('BRK'))
  player_pf = Player('Panicfish', bm.get_simple_bot('PF'))
  player_dk = Player('Danceking', bm.get_simple_bot('DK'))
  player_sf = Player('Stockfish', bm.get_simple_bot('SF'))
  player_sns = Player('Sensitive', bm.get_simple_bot('SNS'))


  # experiment players:
  bot_sf_dk = WaterBot(bm.get_simple_bot('SF'), bm.get_simple_bot('DK'), 0.25)
  bot_sf_brk = WaterBot(bm.get_simple_bot(
      'SF'), bm.get_simple_bot('BRK'), 0.25)
  bot_sf_dc_sk_brk = WaterBot(bot_sf_brk, bot_sf_dk, 0.5)

  player_sf_lotto = Player("Lotto", bot_sf_dc_sk_brk)

  player_brk_m = Player('Berserk SF', BerserkModularBot(bm.get_simple_bot('SF')))

  # quiet players not hving explicit games played
  lineup_quiet = [
      # player_ar,
      # player_sk,
      # player_pc,
      # player_sf_lotto,
      # player_brk,
  ]

  lineup_performing = [
      player_ar,
      player_sk,
      player_pc,
      player_sns,
      player_brk_m,
      player_sf
  ]

  # standard lineup is added quietly
  
  NAME = 'bot_experiment'
  tourney = Tourney(NAME, 10, bm)
  tourney.add_players_quiet(lineup_quiet)

  tourney.continue_tourney_multi(lineup_performing)
  dao.store_tourney(tourney)


if __name__ == '__main__':
  bm = BotManager()
  dao = RecordsDao(bm)

  # dao_cont_1(dao, bm)
  # dao_cont_2(dao, bm)
  # dao_cont_3(dao, bm)
  # dao_cont_cleanup(dao)

  run_tourney_store_db(dao, bm)
  # bot_manager_export_test(bm)
  # quiet_continue_stanard_test(bm)

  bm.engine.close()
  dao.client.close()
