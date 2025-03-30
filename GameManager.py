import random
import pygame
import time
from constant import CELL_SIZE, BLACK, WHITE, RED
from player import Player
from maze import Maze
import csv


class GameManager:
    def __init__(self, rows, cols, player_name, num_keys=3, extra_paths=10):
        self.maze = Maze(rows, cols, num_keys, extra_paths)
        self.player = Player(player_name)
        self.start_time = time.time()
        self.end_time = None
        self.game_state = "playing"

    def draw(self, screen):
        self.maze.draw_maze(screen, self.player.collected_keys, self.player)
        pygame.draw.rect(screen, RED, (self.maze.end_pos[0] * CELL_SIZE, self.maze.end_pos[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE))

    def update(self, dx, dy):
        if self.player.move(dx, dy, self.maze):
            key_collected = self.player.check_key_collection(self.maze)
            if key_collected is not None:
                print(f"{self.player.name} collected a key!")

            if self.player.reached_end(self.maze.end_pos) and self.player.has_all_keys(self.maze):
                self.end_time = time.time()
                self.game_state = "win"
                self.save_game_data()
                return "win"
        return "playing"

    def save_game_data(self):
        time_taken = round(self.end_time - self.start_time, 2) if self.end_time else 0
        data = [self.player.name, time_taken, len(self.player.collected_keys)]
        with open("game_results.csv", mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(data)
        print(f"Game data saved: {data}")

    def reset_game(self):
        self.player.respawn()
        self.player.collected_keys.clear()
        self.start_time = time.time()
        self.game_state = "playing"
        self.maze = Maze(self.maze.rows, self.maze.cols, self.maze.num_keys)
