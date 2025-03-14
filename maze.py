import random
import pygame
from constant import CELL_SIZE, BLACK, WHITE


class Maze:
    def __init__(self, rows, cols, num_keys=3):
        self.rows = rows
        self.cols = cols
        self.maze = self.generate_maze_backtracking()
        self.end_pos = self.find_valid_end_position()
        self.num_keys = num_keys
        self.key_positions = self.place_random_keys(num_keys)

    def generate_maze_backtracking(self):
        maze = [[1] * self.cols for _ in range(self.rows)]
        stack = [(0, 0)]
        visited = set(stack)

        while stack:
            x, y = stack[-1]
            maze[y][x] = 0
            neighbors = [(x + dx, y + dy) for dx, dy in [(0, 2), (2, 0), (-2, 0), (0, -2)]]
            random.shuffle(neighbors)
            for nx, ny in neighbors:
                if 0 <= nx < self.cols and 0 <= ny < self.rows and (nx, ny) not in visited:
                    maze[(y + ny) // 2][(x + nx) // 2] = 0
                    stack.append((nx, ny))
                    visited.add((nx, ny))
                    break
            else:
                stack.pop()
        return maze

    def find_valid_end_position(self):
        for y in range(self.rows - 1, -1, -1):
            for x in range(self.cols - 1, -1, -1):
                if self.maze[y][x] == 0:
                    return x, y
        return self.cols - 1, self.rows - 1

    def place_random_keys(self, count):
        keys = []
        attempts = 0
        max_attempts = 1000  # Prevent infinite loop

        while len(keys) < count and attempts < max_attempts:
            x, y = random.randint(0, self.cols - 1), random.randint(0, self.rows - 1)
            # Avoid start, end position, other keys, and walls
            if self.maze[y][x] == 0 and (x, y) not in [(0, 0), self.end_pos] and (x, y) not in keys:
                keys.append((x, y))
            attempts += 1

        return keys

    def draw_maze(self, screen, collected_keys, player):
        # Draw maze grid
        for y in range(self.rows):
            for x in range(self.cols):
                color = BLACK if self.maze[y][x] == 0 else WHITE
                pygame.draw.rect(screen, color, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))

        # Draw exit
        exit_image = pygame.image.load("exit.png")
        exit_image = pygame.transform.scale(exit_image, (CELL_SIZE, CELL_SIZE))
        screen.blit(exit_image, (self.end_pos[0] * CELL_SIZE, self.end_pos[1] * CELL_SIZE))

        # Draw keys that haven't been collected yet
        key_image = pygame.image.load("key.png")
        key_image = pygame.transform.scale(key_image, (CELL_SIZE, CELL_SIZE))

        for i, key_pos in enumerate(self.key_positions):
            if i not in collected_keys:  # Only draw keys that haven't been collected
                screen.blit(key_image, (key_pos[0] * CELL_SIZE, key_pos[1] * CELL_SIZE))

        # Draw player
        bot_image = pygame.image.load("robot.png")
        bot_image = pygame.transform.scale(bot_image, (CELL_SIZE, CELL_SIZE))
        screen.blit(bot_image, (player.x * CELL_SIZE, player.y * CELL_SIZE))

    def is_valid_move(self, x, y):
        return 0 <= x < self.cols and 0 <= y < self.rows and self.maze[y][x] == 0