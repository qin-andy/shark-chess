# -*- coding: utf-8 -*-
"""Shark Chess.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/10k5gCzjk2CR84qOzExWf66O-xwOva5Ig

# Computer Chess Tourney

## Imports and Packages
"""

import random
import time
import typing
import math

import matplotlib.pyplot as plt

import numpy as np
import pandas as pd

import chess
import chess.svg
import chess.engine
import chess.pgn


"""## Testing Chess Package

Stockfish vs Random Moves
"""

stockfish_path = '../stockfish/stockfish_15.1_win_x64_popcnt/stockfish_15.1_win_x64_popcnt/stockfish-windows-2022-x86-64-modern.exe'

"""## Concrete Bot Setup"""

engine = chess.engine.SimpleEngine.popen_uci(stockfish_path)

base_limit = chess.engine.Limit(time=0.1, depth=10)

bot_ar = AlwaysRandomBot()
bot_sf = Stockfish100Bot(engine, base_limit)
bot_berserk = BerserkBot()
bot_panic = PanicFishBot(engine, base_limit)
bot_pacifist = PacifistBot()
bot_dance_king = DanceKingBot()
bot_suicide_king = SuicideKingBot()

# Water Bot levels
water_fish_80 = WaterBot(bot_sf, bot_ar, 0.8)
water_fish_80.custom_name = "WaterFish80"

water_fish_30 = WaterBot(bot_sf, bot_ar, 0.3)
water_fish_30.custom_name = "WaterFish30"

# Sharkfish
shark_fish = SharkFishBot(bot_ar, 0, 5, engine, base_limit)

# Test a game
game_result = play_game(bot_pacifist, bot_suicide_king, 500)
print(game_result.pc_board.outcome())

board_svg = chess.svg.board(game_result.pc_board)
# display(game_result.pc_board)
print(game_result.pc_game)

"""# Match Running

## Elo Calcuations
"""


# Actually play the games

"""## Run Bot Tournament


"""

# Initializing bots
base_limit = chess.engine.Limit(time=0.1, depth=10)

shark_angry = SharkFishBot(bot_berserk, 0, 3, engine, base_limit)
shark_angry.custom_name = "BerserkShark"

shark_lurk = SharkFishBot(bot_berserk, 2, 7, engine, base_limit)
shark_lurk.custom_name = "LurkShark"

torrent_80 = WaterBot(bot_sf, bot_berserk, 0.8)
torrent_80.custom_name = 'Torrent80'

# bots_x = [bot_dance_king, bot_suicide_king, bot_ar, bot_pacifist, bot_berserk,
#           shark_angry, shark_lurk,
#           torrent_80, water_fish_80, bot_sf,
#           bot_panic]

bots_x = [bot_dance_king, bot_suicide_king]
# Setting up required resources
player_names = []
elos = {}
for bot in bots_x:
  player_names.append(str(bot))
  elos[str(bot)] = 800
print(player_names)

engine.close()

### PLAY THE TOURNAMENT!
game_results = play_tournament(bots_x, 1, False)

# Bot Names for Labelling


