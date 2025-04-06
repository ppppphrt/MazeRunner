
import csv
import os

class Leaderboard:
    def __init__(self, file_path="leaderboard.csv"):
        """Initialize the leaderboard with a CSV file."""
        self.file_path = file_path
        # Ensure file exists with headers
        if not os.path.exists(self.file_path):
            with open(self.file_path, mode="w", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(["Player Name", "Score", "Time Taken"])

    def save_score(self, player_name, score, time_taken):
        """Save a player's score to the CSV file."""
        with open(self.file_path, mode="a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([player_name, score, time_taken])

    def load_scores(self):
        """Load all scores from the CSV file, sorted by best score (lower time is better)."""
        scores = []
        with open(self.file_path, mode="r") as file:
            reader = csv.reader(file)
            next(reader)  # Skip the header
            scores = sorted(reader, key=lambda row: (int(row[1]), float(row[2])))  # Sort by score then time

        return scores

    def get_top_scores(self, limit=5):
        """Return the top 'limit' scores from the leaderboard."""
        scores = self.load_scores()
        return scores[:limit]

