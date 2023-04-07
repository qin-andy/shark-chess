
import os
from typing import Dict, List
from bots.simple_bots import *
from bots.composite_bots import *

import chess
import chess.engine

# Bot manager used to handle bots. 3 main use cases
# 1. give a simple way of constructing all the necessary bots
# 2. Tourney continuation: lookup table for simple bots
# 3. Tourney continuation: creates composite bots per bot settings.
class BotManager:
  base_limit = chess.engine.Limit(time=0.1, depth=10)

  # Two categories of bots
  # Simple bots have no configuration settings and can be constructed as is
  # Composite bots have config settings passed in through
  def __init__(self):
    # Initializing simple bots
    bot_ar = AlwaysRandomBot()
    bot_sk = SuicideKingBot()
    bot_pacifist = PacifistBot()
    bot_berserk = BerserkBot()
    bot_dance = DanceKingBot()

    # Stockfish bots
    # for testing, you can manually set self.engine to give custom engine. otherwise, creates one.
    stockfish_path = '../../stockfish/stockfish-ubuntu-20.04-x86-64' # TODO : refactor
    dirname = os.path.dirname(__file__)
    filename = os.path.join(dirname, stockfish_path)
    engine = chess.engine.SimpleEngine.popen_uci(filename) # TODO : should close this after continuing tourney
    self.engine = engine

    base_limit = self.base_limit
    
    bot_sf = Stockfish100Bot(self.engine, base_limit)
    bot_panic = PanicFishBot(self.engine, base_limit)
    bot_sns = SensitiveFish(self.engine, base_limit)


    # Simple bots are preconstructed as above, and accessed through loopkup table
    simple_bots_map: Dict[str, ChessBot] = { # TODO : could we make code a static field?
      bot_ar.code: bot_ar,
      bot_sk.code: bot_sk,
      bot_pacifist.code: bot_pacifist,
      bot_berserk.code: bot_berserk,
      bot_sf.code: bot_sf,
      bot_panic.code: bot_panic,
      bot_dance.code: bot_dance,
      bot_sns.code: bot_sns,
    }

    if '0' in simple_bots_map.keys():
      codeless_bot = simple_bots_map['0']
      raise Exception('Empty bot detected: ' + str(codeless_bot))

    self.simple_bots_map = simple_bots_map

    composite_bot_codes: List[str] = [
      WaterBot.code,
      SharkFishBot.code
    ]

    self.composite_bot_codes = composite_bot_codes
  
  # Bots should be accessed primarily through here.
  # Simple bot codes: retrieves bot from lookup table
  # Composite bot codes: requires settings. constructs a new bot according to settings
    # Will call itself recuyrsively for composite bots.
    # Depth: used to limit recursive calls  
  def get_bot(self, settings: dict, depth: int=0):
    if depth >= 6: 
      raise Exception('Max composite bot depth reacched!')
    
    code = settings['Code']

    if code in self.simple_bots_map.keys():
      return self.simple_bots_map[code]
    if code in self.composite_bot_codes:
      if settings == None:
        raise Exception ('Missing settings for bot ' + code)
      # Casework
      if code == 'WB':
        print('smubbis')
        # TODO : casework for loading WB
        b1 = self.get_bot(settings['b1'])
        b2 = self.get_bot(settings['b2'])
        return WaterBot(b1, b2, settings['ratio'])
        
    raise Exception('Code not in bot manager: ' + str(code))
  
  # shorthand for simple bots by code
  def get_simple_bot(self, code: str):
    return self.get_bot({'Code': code})