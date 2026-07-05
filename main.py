import random

def init():
  global cheatChance
  print(f'''
Explanation: https://youtu.be/XTcP4oo4JI4
Fair players get a coin that flips to heads 50% of the time.
Cheaters get a coin that flips to heads 75% of the time.

True negatives: Fair players that were correctly detected as fair.
False negatives: Unfair players that were incorrectly detected as fair.
True positives: Unfair players that were correctly detected as unfair.
False positives: Fair players that were incorrectly detected as unfair.

False Positive Rate: False positives / Total fair players.
True Positive Rate: True positives / Total unfair players.
Threshold: The number of heads at which a player is guessed to be cheating (greater than or equal to threshold is guessed to be cheating)
Statistical Power: Threshold / Total flips

The goal is to minimize the {bold('False Positive Rate')} and maximize the {bold('True Positive Rate')}.
Or in other words, to falsely accuse as few players as possible whilst catching as many cheaters as possible.
This involves finding the ideal {bold('Statistical Power')} at a certain number of flips.
One last constraint - Minimize the number of coin flips necessary to determine fairness. The limits the utilization of the Law of Large Numbers and increases the practicality of real-life application.
      ''')
  goalRate1 = getN(f"Maximum {bold('False Positive Rate')} (default = 0.05): ", 0.05)
  goalRate2 = getN(f"Minimum {bold('True Positive Rate')} (default = 0.8): ", 0.8)
  players = getN("Number of players to simulate (default = 100): ", 100.0)
  #bias = getN("Bias (percent players that are cheating - default = 0.5 (or 50%)): ", 0.5)
  bias = None
  cheatChance = getN("Cheater chance of getting heads (default = 0.75): ", 0.75)
  ideals = find(goalRate1, goalRate2, players, bias)
  print(f'''\n
RESULTS
-------
Ideal flips: {ideals[0]}
Ideal Threshold: {ideals[1]}
Ideal Statistical Power: {ideals[1] / ideals[0]}

Constraints:
False Positive Rate: {goalRate1}
True Positive Rate: {goalRate2}
Conditions:
False Positive Rate: {ideals[2]}
True Positive Rate: {ideals[3]}
Cheater chance of heads: {cheatChance}
        ''')

cheatChance = 0.75

class Player:
  def __init__(self, bias = 0.5):
    global cheatChance
    if ((random.randrange(1, 100) / 100) < bias): self.isCheater = False
    else: self.isCheater = True
    self.heads = 0
    self.tails = 0
    if (self.isCheater): self.chance = cheatChance
    else: self.chance = 0.5
  def flip(self, n = 1):
    for x in range(n):
      if ((random.randrange(1, 100) / 100) < self.chance): self.heads += 1
      else: self.tails += 1

def simulate(flips = 10, players = 100, threshold = 7, bias = 0.5):
  tN = 0 # True negatives
  fN = 0 # False negatives
  tP = 0 # True positives
  fP = 0 # False positives
  correct = 0
  incorrect = 0
  for n in range(int(players)):
    if (bias == None): p = Player(n % 2)
    else: p = Player(bias)
    p.flip(flips)
    guess = False
    if (p.heads > threshold): guess = True
    if (p.isCheater):
      if (guess): tP += 1
      else: fN += 1
    else:
      if (guess): fP += 1
      else: tN += 1
    if (p.isCheater == guess): correct += 1
    else: incorrect += 1
    del p
  falsePositiveRate = fP / (fP + tN)
  truePositiveRate = tP / (tP + fN)
  return {
    "tN": tN,
    "fN": fN,
    "tP": tP,
    "fP": fP,
    "correct": correct,
    "incorrect": incorrect,
    "falsePositiveRate": falsePositiveRate,
    "truePositiveRate": truePositiveRate
  }

def find(g1, g2, players, bias, maxFlips = 100):
  for flips in range(maxFlips - 99, maxFlips):
    for threshold in range(flips//2, flips):
      sim = simulate(flips, players, threshold, bias)
      print("\n" + str(sim), "\n\tFlips: " + str(flips), "| Threshold: " + str(threshold), "| Statistical Power: " + str(threshold / flips))
      #print(f"fP Rate of {sim['falsePositiveRate']} and tP Rate of {sim['truePositiveRate']} with {flips} flips, a threshold of {threshold}, and a Statistical Power of {threshold/flips}.")
      if (sim["falsePositiveRate"] <= g1 and sim["truePositiveRate"] >= g2):
        return [flips, threshold, sim["falsePositiveRate"], sim["truePositiveRate"]]
  return find(g1, g2, players, bias, maxFlips + 100)

def bold(txt):
  return '\033[1m' + txt + '\033[0m'

def getN(prompt, default):
  n = input(prompt)
  try:
    n = float(n)
  except:
    return default
  if (n > 1 and default < 1): return default
  return n

init()