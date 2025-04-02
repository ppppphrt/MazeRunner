import os
import random
import pygame
import time
from constant import CELL_SIZE, BLACK, WHITE, RED
from player import Player
from maze import Maze
import csv
import Leaderboard


class GameManager:
    def __init__(self, results_file="game_results.csv"):
        """Initialize the game manager with a results file."""
        self.results_file = results_file
        # Ensure file exists with headers
        if not os.path.exists(self.results_file):
            with open(self.results_file, mode="w", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(["Time Taken"])

    def save_time(self, time_taken):
        """Save the player's time taken to game_results.csv."""
        with open(self.results_file, mode="a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([time_taken])
