# Minesweeper with Q-Learning

This project implements a Minesweeper game with a reinforcement learning agent using Q-learning. The agent learns to play Minesweeper by interacting with the environment and updating its Q-values based on the rewards it receives.

## Requirements

* Python 3.x
* Pygame
* NumPy

## How to Run

1. Make sure you have the required libraries installed (`pygame` and `numpy`). If not, you can install them using pip:
   ```bash
   pip install pygame numpy


## Code Overview

### Minesweeper Environment (`MinesweeperEnv`)

* **`__init__`:** Initializes the game grid, places mines randomly, and calculates the numbers for each cell.
* **`place_mines`:** Randomly places mines on the grid.
* **`calculate_numbers`:** Calculates the number of adjacent mines for each cell.
* **`count_adjacent_mines`:** Counts the number of mines adjacent to a given cell.
* **`reset`:** Resets the game environment.
* **`step`:** Takes an action (clicking a cell) and returns the new state, reward, and whether the game is over.
* **`reveal_cell`:** Reveals a cell and recursively reveals empty adjacent cells.
* **`get_state`:** Returns a representation of the game state.
* **`draw`:** Draws the game board using Pygame.

### Q-Learning Agent (`QLearningAgent`)

* **`__init__`:** Initializes the Q-table, learning rate, discount factor, and epsilon (exploration rate).
* **`get_q_value`:** Retrieves the Q-value for a given state-action pair.
* **`choose_action`:** Chooses an action based on the epsilon-greedy policy.
* **`get_valid_actions`:** Returns a list of valid actions (unrevealed cells).
* **`learn`:** Updates the Q-value for the given state-action pair based on the reward and the next state.

### Main Game Loop

* Creates an instance of the `MinesweeperEnv` and `QLearningAgent`.
* Runs the game loop, handling user input and updating the game state.
* The agent learns from each action and updates its Q-table.

## Key Concepts

* **Q-Learning:** A model-free reinforcement learning algorithm that learns an optimal policy by estimating the value of taking an action in a given state.
* **Epsilon-Greedy Policy:** A balance between exploration (choosing random actions) and exploitation (choosing the action with the highest Q-value).
* **Rewards:** Used to guide the agent's learning process. In this case, the agent receives positive rewards for revealing safe cells and negative rewards for hitting mines or clicking already revealed cells.
