import csv
import os


class GameManager:
    def __init__(self, results_file="game_results_stat.csv"):
        self.results_file = results_file
        self.stats = {
            "time_taken": 0,
            "keys_collected": 0,
            "steps_taken": 0,
            "wall_collisions": 0,
            "enemy_encounters": 0
        }

        if not os.path.exists(self.results_file):
            with open(self.results_file, mode="w", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(self.stats.keys())

    def record_time(self, elapsed_time):
        self.stats["time_taken"] = int(elapsed_time)

    def record_step(self):
        self.stats["steps_taken"] += 1

    def record_key(self, collected_key):
        self.stats["keys_collected"] = collected_key

    def record_wall_collision(self):
        self.stats["wall_collisions"] += 1

    def record_enemy_encounter(self):
        self.stats["enemy_encounters"] += 1

    def save_stats(self):
        with open(self.results_file, mode="a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(self.stats.values())

    def reset_stats(self):
        for key in self.stats:
            self.stats[key] = 0
