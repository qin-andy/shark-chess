from src.bots.bots import *
from src.tourney.tourney import *

def player_game_test():
  bot_ar = AlwaysRandomBot()
  bot_sk = SuicideKingBot()
  bot_pacifist = PacifistBot()

  player_ar = Player(bot_ar, "RandomPlayer")
  player_sk = Player(bot_sk, "SKPlayer")
  player_pacifist = Player(bot_pacifist, "PacifistPlayer")

  players = [player_sk, player_ar, player_pacifist]
  # gr = play_game(player_sk, player_pacifist, 300)
  # play_match(player_pacifist, player_sk, 5, True)
  tourney = TourneyManager(players, 3)
  tourney.play_tournament()
  tourney.to_csv()


if __name__ == '__main__':
  # play_test_game()
  # play_test_match()
  # play_test_tourney()
  player_game_test()


