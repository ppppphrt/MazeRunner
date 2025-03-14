import pygame
from constant import ROWS, COLS

class Player:

    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y
        self.has_key = False

    def move(self, dx, dy, maze):
        new_x, new_y = self.x + dx, self.y + dy
        if maze.is_valid_move(new_x, new_y):
            self.x, self.y = new_x, new_y
            return True
        return False

    def collect_key(self, key_pos):
        if key_pos and (self.x, self.y) == key_pos:
            self.has_key = True
            return True
        return False

    def reached_end(self, end_pos):
        return (self.x, self.y) == end_pos
