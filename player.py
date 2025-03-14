import pygame
from constant import ROWS, COLS

class Player:
    def __init__(self):
        self.x, self.y = 0, 0  # Start position
        self.has_key = False  # Track if player collected the key

    def move(self, dx, dy, maze):
        """Move player if the destination is an open path (0 in the maze)."""
        new_x, new_y = self.x + dx, self.y + dy
        if 0 <= new_x < COLS and 0 <= new_y < ROWS and maze[new_y][new_x] == 0:
            self.x, self.y = new_x, new_y

    def collect_key(self, key_pos):
        """Check if the player collects the key."""
        if (self.x, self.y) == key_pos:
            self.has_key = True
            return True  # Key collected
        return False

    def reached_end(self, end_pos):
        """Check if player reached the exit."""
        return (self.x, self.y) == end_pos
