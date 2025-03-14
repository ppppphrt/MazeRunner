import pygame

from constant import ROWS, COLS, RED, CELL_SIZE
from maze import Maze
from player import Player


class GameManager:
    def __init__(self, rows = ROWS, cols = COLS):
        self.maze = Maze(rows, cols)
        self.player = Player()
        self.key_pos = self.maze.place_random_item(1)[0] if self.maze.place_random_item(1) else None
        self.end_pos = (cols - 1, rows - 1)

    def draw(self, screen):
        self.maze.draw_maze(screen, self.key_pos if not self.player.has_key else None, self.player)
        # Draw end position
        pygame.draw.rect(screen, RED, (self.end_pos[0] * CELL_SIZE, self.end_pos[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE))

    def update(self, dx, dy):
        if self.player.move(dx, dy, self.maze):
            if self.player.collect_key(self.key_pos):
                self.key_pos = None

            if self.player.reached_end(self.end_pos) and self.player.has_key:
                return "win"
        return "playing"