from src.bots.bots import AlwaysRandomBot, SuicideKingBot, PacifistBot
from src.tourney.tourney import play_game, play_match, play_tournament


def play_test_game():
  bot_ar = AlwaysRandomBot()
  bot_sk = SuicideKingBot()
  game_result = play_game(bot_ar, bot_sk, 500)
  print(game_result.pc_board.outcome())
  print(game_result.pgn)
  # board_svg = chess.svg.board(game_result.pc_board)


def play_test_match():
  bot_ar = AlwaysRandomBot()
  bot_sk = SuicideKingBot()
  game_results = play_match(bot_ar, bot_sk, 3)
  print(str(game_results))
  print(game_results[0])


def play_test_tourney():
  bot_ar = AlwaysRandomBot()
  bot_sk = SuicideKingBot()
  bot_pacifist = PacifistBot()

  bots = [bot_ar, bot_sk, bot_pacifist]

  game_results = []
  player_names = []
  elos = {}
  for bot in bots:
    player_names.append(str(bot))
    elos[str(bot)] = 800
  print(player_names)
  play_tournament(bots, 3, bots, elos)


if __name__ == '__main__':
  play_test_game()
  play_test_match()
  play_test_tourney()
