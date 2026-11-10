# Statistical Fairness Simulation

A simulation tool for finding the optimal strategy to detect cheaters in a coin-flipping game, based on [this video](https://youtu.be/XTcP4oo4JI4).

## How it works

- **Fair players** flip a coin with a 50% chance of heads
- **Cheaters** flip a coin with a 75% chance of heads (configurable)

The simulator finds the ideal number of flips and a **threshold** (minimum heads count to flag someone as a cheater) that satisfies two constraints:

- **False Positive Rate** — how often fair players are wrongly accused (minimize this)
- **True Positive Rate** — how often cheaters are correctly caught (maximize this)

## Usage

```bash
python main.py
```

You will be prompted to enter:
- Maximum acceptable False Positive Rate (default: 0.05)
- Minimum acceptable True Positive Rate (default: 0.80)
- Number of players to simulate (default: 100)
- Cheater's chance of getting heads (default: 0.75)

The program then outputs the ideal number of flips, threshold, and statistical power.

## Requirements

- Python 3.8
- numpy
