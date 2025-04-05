import random
import pygame
from constant import CELL_SIZE, BLACK, WHITE


class Maze:
    def __init__(self, rows, cols, num_keys=3, extra_paths=10):
        self.rows = rows
        self.cols = cols
        self.maze = self.generate_maze_prims()
        self.add_extra_paths(extra_paths)
        self.add_extra_paths(extra_paths // 2)  # Add even more alternative paths
        self.end_pos = self.find_valid_end_position()
        self.num_keys = num_keys
        self.key_positions = self.place_random_keys(num_keys)

    # def generate_maze_backtracking(self):
    #     maze = [[1] * self.cols for _ in range(self.rows)]
    #     stack = [(0, 0)]
    #     visited = set(stack)
    #
    #     while stack:
    #         x, y = stack[-1]
    #         maze[y][x] = 0
    #         neighbors = [(x + dx, y + dy) for dx, dy in [(0, 2), (2, 0), (-2, 0), (0, -2)]]
    #         random.shuffle(neighbors)
    #         for nx, ny in neighbors:
    #             if 0 <= nx < self.cols and 0 <= ny < self.rows and (nx, ny) not in visited:
    #                 maze[(y + ny) // 2][(x + nx) // 2] = 0
    #                 stack.append((nx, ny))
    #                 visited.add((nx, ny))
    #                 break
    #         else:
    #             stack.pop()
    #     return maze

    def generate_maze_prims(self):
        """Generate a maze using Prim's Algorithm."""
        maze = [[1] * self.cols for _ in range(self.rows)]  # Start with all walls
        walls = []

        # Pick a random starting point
        start_x, start_y = random.randrange(0, self.cols, 2), random.randrange(0, self.rows, 2)
        maze[start_y][start_x] = 0  # Mark starting cell as a passage

        # Add surrounding walls to the list
        directions = [(0, 2), (2, 0), (-2, 0), (0, -2)]
        for dx, dy in directions:
            nx, ny = start_x + dx, start_y + dy
            if 0 <= nx < self.cols and 0 <= ny < self.rows:
                walls.append((nx, ny, start_x, start_y))

        while walls:
            wx, wy, px, py = random.choice(walls)  # Pick a random wall
            walls.remove((wx, wy, px, py))

            if maze[wy][wx] == 1:  # If it's still a wall
                maze[wy][wx] = 0  # Make it a passage
                maze[(wy + py) // 2][(wx + px) // 2] = 0  # Open path between cells

                # Add neighboring walls to the list
                for dx, dy in directions:
                    nx, ny = wx + dx, wy + dy
                    if 0 <= nx < self.cols and 0 <= ny < self.rows and maze[ny][nx] == 1:
                        walls.append((nx, ny, wx, wy))

        return maze

    def add_extra_paths(self, count):
        attempts = 0
        while count > 0 and attempts < 2000:  # Increase attempts for better distribution
            x, y = random.randint(1, self.cols - 2), random.randint(1, self.rows - 2)
            if self.maze[y][x] == 1 and sum(self.maze[ny][nx] == 0 for nx, ny in [(x-1, y), (x+1, y), (x, y-1), (x, y+1)]) >= 1:
                self.maze[y][x] = 0
                count -= 1
            attempts += 1

    def find_valid_end_position(self):
        for y in range(self.rows - 1, -1, -1):
            for x in range(self.cols - 1, -1, -1):
                if self.maze[y][x] == 0:
                    return x, y
        return self.cols - 1, self.rows - 1

    def place_random_keys(self, count):
        keys = []
        attempts = 0
        max_attempts = 1000

        while len(keys) < count and attempts < max_attempts:
            x, y = random.randint(0, self.cols - 1), random.randint(0, self.rows - 1)
            if self.maze[y][x] == 0 and (x, y) not in [(0, 0), self.end_pos] and (x, y) not in keys:
                keys.append((x, y))
            attempts += 1

        return keys

    def draw_maze(self, screen, collected_keys, player, y_offset=0):
        for y in range(self.rows):
            for x in range(self.cols):
                color = WHITE if self.maze[y][x] == 0 else BLACK
                pygame.draw.rect(screen, color, (x * CELL_SIZE, y * CELL_SIZE + y_offset, CELL_SIZE, CELL_SIZE))

        exit_image = pygame.image.load("pic/exit.png")
        exit_image = pygame.transform.scale(exit_image, (CELL_SIZE, CELL_SIZE))
        screen.blit(exit_image, (self.end_pos[0] * CELL_SIZE, self.end_pos[1] * CELL_SIZE))

        key_image = pygame.image.load("pic/key.png")
        key_image = pygame.transform.scale(key_image, (CELL_SIZE, CELL_SIZE))
        for i, key_pos in enumerate(self.key_positions):
            if i not in collected_keys:
                screen.blit(key_image, (key_pos[0] * CELL_SIZE, key_pos[1] * CELL_SIZE))

        bot_image = pygame.image.load("pic/robot.png")
        bot_image = pygame.transform.scale(bot_image, (CELL_SIZE, CELL_SIZE))
        screen.blit(bot_image, (player.x * CELL_SIZE, player.y * CELL_SIZE))

    def is_valid_move(self, x, y):
        return 0 <= x < self.cols and 0 <= y < self.rows and self.maze[y][x] == 0
