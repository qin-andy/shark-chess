
import pandas as pd
from pymongo import MongoClient
import os

cwd = os.getcwd()
print(cwd)

# Connect to port
client = MongoClient('localhost', 27017)

# Create/Access DB
db_name = 'shark-chess'
db = client[db_name]
games_collec = db['games']
players_collec = db['players']
games_collec.drop() # drops prexisting games
players_collec.drop()

games_df = pd.read_csv('game_output.csv')
players_df = pd.read_csv('player_output.csv')

games = games_df.to_dict('records')
games_collec.insert_many(games)


players = players_df.to_dict('records')
players_collec.insert_many(players)

client.close()