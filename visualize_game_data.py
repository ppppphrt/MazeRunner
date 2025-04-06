import pandas as pd
import matplotlib.pyplot as plt

# Load the data
df = pd.read_csv("game_results_stat.csv")

# --- 1. Table comparison: Time Taken (min, max) ---
min_time = df["time_taken"].min()
max_time = df["time_taken"].max()

print("=== Time Taken Comparison ===")
print(f"Minimum Time Taken: {min_time} seconds")
print(f"Maximum Time Taken: {max_time} seconds")
print()

# --- 2. Bar Chart: Average Keys Collected and Wall Collisions ---
avg_keys = df["keys_collected"].mean()
avg_collisions = df["wall_collisions"].mean()

plt.figure(figsize=(6, 4))
plt.bar(["Keys Collected", "Wall Collisions"], [avg_keys, avg_collisions], color=["skyblue", "salmon"])
plt.title("Average Keys Collected & Wall Collisions")
plt.ylabel("Average Count")
plt.tight_layout()
plt.savefig("bar_chart_avg_keys_collisions.png")
plt.show()

# --- 3. Line Chart: Steps Taken & Enemy Encounters Over Time ---
plt.figure(figsize=(8, 5))
plt.plot(df["steps_taken"], label="Steps Taken", marker="o", color="green")
plt.plot(df["enemy_encounters"], label="Enemy Encounters", marker="x", color="red")
plt.title("Steps and Enemy Encounters Over Sessions")
plt.xlabel("Game Session")
plt.ylabel("Count")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig("line_chart_steps_enemy.png")
plt.show()
