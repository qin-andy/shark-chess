
import pandas as pd
from pymongo import MongoClient
import os
from bson.json_util import dumps


cwd = os.getcwd()
print(cwd)

# Connect to port
client = MongoClient('localhost', 27017)

# Create/Access DB
db_name = 'shark-chess'
db = client[db_name]
games_collec = db['games']
players_collec = db['players']


# Dump as json
indent = 2

games_cursor = games_collec.find()
games_list = list(games_cursor)
games_json = dumps(games_list, indent=indent)


with open('games.json', 'w') as file:
    file.write(games_json)

players_cursor = players_collec.find()
players_list = list(players_cursor)
players_json = dumps(players_list, indent=indent)

with open('players.json', 'w') as file:
    file.write(players_json,)

