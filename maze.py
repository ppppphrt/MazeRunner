import random
import pygame
from constant import CELL_SIZE, BLACK, WHITE , RED


class Maze:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.maze = self.generate_maze_backtracking()
        self.end_pos = self.find_valid_end_position()

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

    def draw_maze(self, screen, key_pos, player):
        for y in range(self.rows):
            for x in range(self.cols):
                color = BLACK if self.maze[y][x] == 0 else WHITE
                pygame.draw.rect(screen, color, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))

        # key
        if key_pos is not None:
            key_image = pygame.image.load("key.png")
            key_image = pygame.transform.scale(key_image, (CELL_SIZE, CELL_SIZE))
            screen.blit(key_image, (key_pos[0] * CELL_SIZE, key_pos[1] * CELL_SIZE))

        # player
        bot_image = pygame.image.load("robot.png")
        bot_image = pygame.transform.scale(bot_image, (CELL_SIZE, CELL_SIZE))
        screen.blit(bot_image, (player.x * CELL_SIZE, player.y * CELL_SIZE))

        # exit
        exit_image = pygame.image.load("exit.png")
        exit_image = pygame.transform.scale(exit_image, (CELL_SIZE, CELL_SIZE))
        screen.blit(exit_image, (self.end_pos[0] * CELL_SIZE, self.end_pos[1] * CELL_SIZE))

    def find_valid_end_position(self):
        for y in range(self.rows - 1, -1, -1):
            for x in range(self.cols - 1, -1, -1):
                if self.maze[y][x] == 0:  # Check if it's a path (0 = BLACK route)
                    return x, y
        return self.cols - 1, self.rows - 1

    def place_random_item(self, item_count):
        items = []
        while len(items) < item_count:
            x, y = random.randint(0, self.cols - 1), random.randint(0, self.rows - 1)
            if self.maze[y][x] == 0 and (x, y) not in [(0, 0), (self.cols - 1, self.rows - 1)]:
                items.append((x, y))
        return items

    def is_valid_move(self, x, y):
        return 0 <= x < self.cols and 0 <= y < self.rows and self.maze[y][x] == 0


