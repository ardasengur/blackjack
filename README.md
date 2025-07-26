# Blackjack Simulation Tool

This program simulates the game of Blackjack for a given player hand and dealer upcard, allowing you to analyze the win, loss, and draw probabilities for both "stand" and "hit" actions. If your hand contains an Ace, the simulation separately considers the Ace as both 1 and 11.

## Features
- Simulates 1000 games for the exact hand and dealer card you specify
- Reports win, loss, and draw rates for both "stand" and "hit" actions
- Separately analyzes scenarios where Ace is counted as 1 or 11
- Simple command-line interface

## Usage
1. Run the program:
   ```
   python main.py
   ```
2. Enter your first card (1-10, Ace as 1) when prompted.
3. Enter your second card (1-10, Ace as 1) when prompted.
4. Enter the dealer's visible card (1-10, Ace as 1) when prompted.

5. The program will simulate 1000 games for each action and print a summary table. In the output table:
   - The action with the highest win rate is marked with a gold star (★).
   - The action with the lowest lose rate ("not lose" best) is marked with a silver star (☆).

   | Action | Win % | Lose % | Draw % | Ace Usage | Note |
   |--------|-------|--------|--------|-----------|------|
   | stand  |  ...  |  ...   |  ...   | Ace as 1  |  ★   |
   | hit    |  ...  |  ...   |  ...   | Ace as 1  |  ☆   |
   | stand  |  ...  |  ...   |  ...   | Ace as 11 |      |
   | hit    |  ...  |  ...   |  ...   | Ace as 11 |      |

## Example Output
```
Enter your first card (1-10, Ace as 1): 1
Enter your second card (1-10, Ace as 1): 7
Enter the dealer's visible card (1-10, Ace as 1): 10

Simulating 1000 games for Player [1, 7] vs Dealer [10, ?]...

Action  |  Win %  |  Lose %  |  Draw %  |  Ace Usage   |  Note
---------------------------------------------------------------
stand   |   34.2  |    58.7  |     7.1  |  Ace as 1    |  
hit     |   23.5  |    71.0  |     5.5  |  Ace as 1    |  
stand   |   41.8  |    51.2  |     7.0  |  Ace as 11   |  ★☆
hit     |   29.7  |    64.1  |     6.2  |  Ace as 11   |  
```

## Requirements
- Python 3.x
- numpy

Install dependencies with:
```
pip install numpy
```

## License
MIT