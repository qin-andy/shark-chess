from pymongo import MongoClient
import os
import json


class RecordsDao:
    def __init__(self) -> None:
      self.client = MongoClient('localhost', 27017)
      self.db = self.client['shark-chess'] # todo : refactor to constants
      self.games = self.db['games']
      self.players = self.db['players']

        
    