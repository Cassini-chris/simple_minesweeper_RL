import pygame
import numpy as np
import random

# --- Pygame Setup ---
width, height = 800, 600
cell_size = 30
grid_width = 10
grid_height = 10
num_mines = 10

pygame.init()
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Minesweeper")

# --- Minesweeper Environment ---
class MinesweeperEnv:
    def __init__(self):
        self.grid = np.zeros((grid_height, grid_width), dtype=int)  # 0: empty, -1: mine
        self.revealed = np.zeros((grid_height, grid_width), dtype=bool)
        self.place_mines()
        self.calculate_numbers()

    def place_mines(self):
        mines_placed = 0
        while mines_placed < num_mines:
            row = random.randint(0, grid_height - 1)
            col = random.randint(0, grid_width - 1)
            if self.grid[row, col] != -1:  # Avoid placing mines on top of each other
                self.grid[row, col] = -1
                mines_placed += 1

    def calculate_numbers(self):
        for row in range(grid_height):
            for col in range(grid_width):
                if self.grid[row, col] != -1:
                    self.grid[row, col] = self.count_adjacent_mines(row, col)

    def count_adjacent_mines(self, row, col):
        count = 0
        for r in range(max(0, row - 1), min(grid_height, row + 2)):
            for c in range(max(0, col - 1), min(grid_width, col + 2)):
                if (r != row or c != col) and self.grid[r, c] == -1:
                    count += 1
        return count

    def reset(self):
        self.__init__()  # Reinitialize the environment
        return self.get_state()

    def step(self, action):
        row, col = action
        if self.revealed[row, col]:
            return self.get_state(), -0.1, False  # Penalty for clicking a revealed cell
        elif self.grid[row, col] == -1:
            self.revealed[row, col] = True
            return self.get_state(), -1, True  # Game over, hit a mine
        else:
            self.reveal_cell(row, col)
            return self.get_state(), 1, False  # Reward for revealing a safe cell

    def reveal_cell(self, row, col):
        self.revealed[row, col] = True
        if self.grid[row, col] == 0:
            for r in range(max(0, row - 1), min(grid_height, row + 2)):
                for c in range(max(0, col - 1), min(grid_width, col + 2)):
                    if not self.revealed[r, c]:
                        self.reveal_cell(r, c)  # Recursively reveal empty cells

    def get_state(self):
        # ... (Return a representation of the game state, e.g., a 2D array) ...
        state = np.zeros((grid_height, grid_width), dtype=int)
        for row in range(grid_height):
            for col in range(grid_width):
                if self.revealed[row, col]:
                    state[row, col] = self.grid[row, col] 
                else:
                    state[row, col] = -2 # -2 represents an unknown cell
        return state

    def draw(self):
        screen.fill((192, 192, 192))  # Background color
        for row in range(grid_height):
            for col in range(grid_width):
                x = col * cell_size
                y = row * cell_size
                rect = pygame.Rect(x, y, cell_size, cell_size)
                pygame.draw.rect(screen, (255, 255, 255), rect, 1)  # Cell border

                if self.revealed[row, col]:
                    if self.grid[row, col] == -1:
                        # Draw a mine
                        pygame.draw.circle(screen, (0, 0, 0), (x + cell_size // 2, y + cell_size // 2), cell_size // 3)
                    elif self.grid[row, col] > 0:
                        # Draw the number
                        font = pygame.font.Font(None, 30)
                        text = font.render(str(self.grid[row, col]), True, (0, 0, 0))
                        text_rect = text.get_rect(center=(x + cell_size // 2, y + cell_size // 2))
                        screen.blit(text, text_rect)
        pygame.display.flip()

# --- Reinforcement Learning Agent (Example: Q-learning) ---
class QLearningAgent:
    def __init__(self, env, learning_rate=0.1, discount_factor=0.9, epsilon=0.1):
        self.env = env
        self.q_table = {}  # Dictionary to store Q-values
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        self.epsilon = epsilon

    def get_q_value(self, state, action):
        state_str = str(state)  # Convert state to a string for dictionary key
        if (state_str, action) not in self.q_table:
            self.q_table[(state_str, action)] = 0  # Initialize Q-value if not seen before
        return self.q_table[(state_str, action)]

    def choose_action(self, state):
        if random.uniform(0, 1) < self.epsilon:
            # Exploration: Choose a random action
            valid_actions = self.get_valid_actions(state)
            return random.choice(valid_actions)
        else:
            # Exploitation: Choose the action with the highest Q-value
            best_action = None
            best_q_value = float('-inf')
            for action in self.get_valid_actions(state):
                q_value = self.get_q_value(state, action)
                if q_value > best_q_value:
                    best_q_value = q_value
                    best_action = action
            return best_action

    def get_valid_actions(self, state):
        valid_actions = []
        for row in range(grid_height):
            for col in range(grid_width):
                if state[row, col] == -2:  # -2 represents an unknown cell
                    valid_actions.append((row, col))
        return valid_actions

    def learn(self, state, action, reward, next_state, done):
        state_str = str(state)
        next_state_str = str(next_state)
        if done:
            target_q_value = reward
            print(reward)
        else:
            best_next_action = self.choose_action(next_state)  # Use current policy to estimate best next action
            target_q_value = reward + self.discount_factor * self.get_q_value(next_state_str, best_next_action)
        
        old_q_value = self.get_q_value(state_str, action)
        self.q_table[(state_str, action)] = old_q_value + self.learning_rate * (target_q_value - old_q_value)

# --- Main Game Loop ---
env = MinesweeperEnv()
agent = QLearningAgent(env)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            col = event.pos[0] 



            row = event.pos[1] // cell_size
            action = (row, col)
            state = env.get_state()  # Get the current state before taking action
            next_state, reward, done = env.step(action)
            agent.learn(state, action, reward, next_state, done)
            if i % 100 == 0:  # Print every 100 steps
                print("Sample Q-values:", list(agent.q_table.items())[:5])  # Print the first 5 Q-value entries
            i += 1
            if done:
                env.reset()  # Reset the game if it's over

    env.draw()  # Draw the game board

pygame.quit()
