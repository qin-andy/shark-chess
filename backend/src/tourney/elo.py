import math

def win_prob(rating1, rating2):
  return 1.0 * 1.0 / (1 + 1.0 * math.pow(10, 1.0 * (rating2 - rating1) / 400))
  # Geeks for geeks was wrong..... their version has a typo int he above alg

# Takes 1 ELO,s a K value, and d = winner == 1
def calculate_elos(rating1, rating2, K, d):
  prob1 = win_prob(rating1, rating2)
  prob2 = win_prob(rating2, rating1)

  # Case 1 When Player A wins
  if d == 1:
    rating1 += K * (1 - prob1)
    rating2 += K * (0 - prob2)

  # Case 2 When Player B wins
  elif d == 0:
    rating1 += K * (0 - prob1)
    rating2 += K * (1 - prob2)

  # Tie case
  else:
    rating1 += K * (0.5 - prob1)
    rating2 += K * (0.5 - prob2)

  return int(rating1), int(rating2)
