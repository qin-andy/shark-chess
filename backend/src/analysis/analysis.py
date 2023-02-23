import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

"""
ANALYSIS FILE

USE GOOGLE COLAB/JUPYTER FOR THIS! 
"""

# Generating DF from elos and game results array
# Need to import/have access to this.
elos = {}
game_results = []

# Data into Pandas
winners = []
reasons = []
moves = []
times = []
pgns = []
whites = []
blacks = []

# Unzip array of game objects into arrays
for gr in game_results:
  winners.append(gr.winner)
  reasons.append(gr.end_reason)
  moves.append(gr.moves)
  times.append(gr.time)
  pgns.append(gr.pgn)
  whites.append(gr.white_player)
  blacks.append(gr.black_player)

# Settingup data in dict
game_data = {
  'Winner': winners,
  'End Reason': reasons,
  'Moves': moves,
  'Time': times,
  'PGN': pgns,
  'White': whites,
  'Black': blacks
}

# Into Pandas :3
df = pd.DataFrame(game_data)
df.to_csv('output.csv', encoding='utf-8-sig')
# files.download('output.csv')

# Summary Analysis of DF
df.groupby("Winner").count()
# Win percents
df['Winner'].value_counts(normalize=True)

"""## Elo Chart"""

print(elos)
kvs = list(elos.items())
kvs.sort(key=lambda x: x[1])
print(kvs)
names_by_elo, elo_values = zip(*kvs)

plt.bar(range(len(elos)), elo_values, tick_label=names_by_elo)
plt.xticks(rotation=90)
# plt.show()
plt.savefig('elos.png')  # TODO : fix sizing

"""## Matchup Chart Creation"""

matchups_dict = {}
round_to_decimals = 3

# overwrite playernames to be sorted by elo
player_names = names_by_elo

for white_player in player_names:
  matchups_dict[white_player] = {}
  for black_player in player_names:
    # Collect all matches from database with white player and black player
    # Consolidate them into stalement and win/loss/staledraw (store as tuple first?)
    # In future, cinlude more info, like average move length
    white_wins = 0.0
    white_drawmates = 0.0
    white_losses = 0.0
    for index, item in df.loc[(df['White'] == white_player) & (df['Black'] == black_player)]['Winner'].value_counts(
            normalize=True).items():
      # Value will be one of white_player, black_player, draw, or Stalement (Stalemate)
      if index == white_player:
        white_wins = round(item, round_to_decimals)
      elif (index == 'Stalemate') or (index == 'Draw'):
        white_drawmates += round(item, round_to_decimals)
    white_losses = round(1 - (white_wins + white_drawmates), round_to_decimals)

    # Append to dict
    matchups_dict[white_player][black_player] = (white_wins, white_drawmates, white_losses)
    # matchups_dict[white_player][black_player] = white_wins
matchups_df = pd.DataFrame(matchups_dict)

ticks = player_names

matchups_rgb = np.array(matchups_df.values.tolist()).astype('float')


def scale_rgb(i):
  new = (i * 0.5) + 0.25
  return i


applyall = np.vectorize(scale_rgb)
matchups_rgb = applyall(matchups_rgb)

plt.figure(figsize=(7, 7))
plt.xlabel("White Player")
plt.ylabel("Black Player")
plt.xticks(range(len(player_names)), player_names, rotation=90)
plt.yticks(range(len(player_names)), player_names)
plt.imshow(matchups_rgb)
# plt.show()
plt.savefig('matchups.png')  # TODO : fix sizing

"""## Time Chart"""

df.loc[(df['White'] == 'Torrent80') & (df['Black'] == 'Torrent80')]['Time'].sum()

matchup_times_dict = {}
for white_player in player_names:
  matchup_times_dict[white_player] = {}
  for black_player in player_names:
    # Collect all matches from database with white player and black player
    # Consolidate them into stalement and win/loss/staledraw (store as tuple first?)
    # In future, cinlude more info, like average move length
    total_time = df.loc[(df['White'] == white_player) & (df['Black'] == black_player)]['Time'].sum()

    # Append to dict
    matchup_times_dict[white_player][black_player] = total_time
    # matchups_dict[white_player][black_player] = white_wins
matchup_times_df = pd.DataFrame(matchup_times_dict)

times_sum = matchup_times_df.sum()
plt.figure(figsize=(12, 4))
plt.xlabel("Player")
plt.ylabel("Time in Seconds")
plt.bar(player_names, times_sum)
plt.xticks(rotation=90)
# plt.show()
plt.savefig('matchup_times.png')  # TODO : fix sizing

plt.pie(times_sum, labels=player_names)
plt.savefig('times_pie_chart.png')

"""## Misc Searches"""

# Selecting rows based on column values, notice use of & instead of and for boolean
df.loc[(df['White'] == 'AlwaysRandom') & (df['Black'] == 'RandShark')]

# Iterating through example
for index, row in df.loc[(df['White'] == 'AlwaysRandom') & (df['Black'] == 'RandShark')].iterrows():
  print(row['Winner'])

# Get Win proportions for a single match
df.loc[(df['White'] == 'AlwaysRandom') & (df['Black'] == 'RandShark')]['Winner'].value_counts(normalize=True)
for index, item in df.loc[(df['White'] == 'AlwaysRandom') & (df['Black'] == 'RandShark')]['Winner'].value_counts(
        normalize=True).items():
  print(index, item)
# Idea: for every both, calculate its win percent against the other bot as the color

df.loc[(df['Winner'] == 'DanceKing')]

# TODO : figure out what to do with this section. refactor?
# """# Playing with Stockfish Depths
#
# ## Testing multiple thinking times with default depth
# """
# eg_sf = Stockfish100Bot(engine, base_limit)
#
# def generate_limits(time_depth_arr):
#   lims = []
#   for time_depth in time_depth_arr:
#     time, depth = time_depth
#     lim = chess.engine.Limit
#     if depth == -1:
#       lim = chess.engine.Limit(time)
#     else:
#       lim = chess.engine.Limit(time, depth)
#     lims.append(lim)
#   return lims
#
# def generate_sf_bots(lims):
#   bots = []
#   for lim in lims:
#     sf = Stockfish100Bot(engine, lim)
#     bots.append(sf)
#   return bots

# time_depths = [
#     (0.1, 2),
#     (0.1, 4),
#     (0.1, 6),
#     (0.1, 8),
#     (0.1, 10),
#     (0.1, 15),
#     (0.1, 20),
#     (0.1, -1)
# ]
#
# lims = generate_limits(time_depths)
# sf_bots = generate_sf_bots(lims)
#
# game_results = play_tournament(sf_bots, 5, False)
#
# player_names = []
# for bot in sf_bots:
#   player_names.append(str(bot))
# print(player_names)