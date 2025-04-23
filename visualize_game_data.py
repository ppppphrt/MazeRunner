from PIL import ImageFont, ImageDraw, Image


def generate_game_stats():
    import pandas as pd
    import matplotlib.pyplot as plt

    df = pd.read_csv("game_results_stat.csv")


    # --- Time Taken (min/max) ---
    min_time = df["time_taken"].min()
    max_time = df["time_taken"].max()

    # Create an image with this info using PIL
    img = Image.new("RGB", (500, 100), color="white")
    draw = ImageDraw.Draw(img)

    # Load a font
    try:
        font = ImageFont.truetype("arial.ttf", 20)
    except:
        font = ImageFont.load_default()

    draw.text((10, 10), "=== Time Taken Comparison ===", fill="black", font=font)
    draw.text((10, 40), f"Minimum Time Taken: {min_time} seconds", fill="black", font=font)
    draw.text((10, 65), f"Maximum Time Taken: {max_time} seconds", fill="black", font=font)

    img.save("/Users/ppppphrt/MazeRunner/stat_pic/time_taken_stat.png")

    # Bar chart
    avg_keys = df["keys_collected"].mean()
    avg_collisions = df["wall_collisions"].mean()
    plt.figure(figsize=(6, 4))
    plt.bar(["Keys Collected", "Wall Collisions"], [avg_keys, avg_collisions], color=["skyblue", "salmon"])
    plt.title("Average Keys Collected & Wall Collisions")
    plt.ylabel("Average Count")
    plt.tight_layout()
    plt.savefig("/Users/ppppphrt/MazeRunner/stat_pic/bar_chart_avg_keys_collisions.png")
    plt.close()

    # Line chart for navigation efficiency analysis
    plt.figure(figsize=(8, 5))
    plt.plot(df["steps_taken"], label="Steps Taken", marker="o", color="green", linewidth=2)
    plt.plot(df["enemy_encounters"], label="Enemy Encounters", marker="x", color="red", linewidth=2)

    # Calculate and plot wall collisions per step (efficiency metric)
    if "wall_collisions" in df.columns:
        plt.plot(df["wall_collisions"], label="Wall Collisions", marker="s", color="orange", linewidth=2)
        efficiency_ratio = df["steps_taken"] / (df["wall_collisions"] + 1)  # Add 1 to avoid division by zero
        plt.plot(efficiency_ratio, label="Steps/Collision Ratio", marker="^", color="purple",
                 linestyle="--", linewidth=1.5)

    plt.title("Navigation Efficiency Analysis", fontsize=14)
    plt.xlabel("Game Session", fontsize=12)
    plt.ylabel("Count / Efficiency Ratio", fontsize=12)
    plt.legend(loc="best")
    plt.grid(True, alpha=0.3)

    # Add annotation about efficiency
    plt.figtext(0.5, 0.01, "Higher steps-to-collision ratio indicates better navigation efficiency",
                ha="center", fontsize=10, style="italic")

    plt.tight_layout()
    plt.savefig("/Users/ppppphrt/MazeRunner/stat_pic/navigation_efficiency_analysis.png")
    plt.close()

    # Bar chart
    avg_wall_col = df["wall_collisions"].mean()
    avg_step = df["steps_taken"].mean()
    plt.figure(figsize=(6, 4))
    plt.bar(["Wall Collisions", "Step Taken"], [avg_wall_col, avg_step], color=["skyblue", "salmon"])
    plt.title("Wall Collisions & Step Taken")
    plt.ylabel("Average Count")
    plt.tight_layout()
    plt.savefig("/Users/ppppphrt/MazeRunner/stat_pic/bar_chart_avg_keys_collisions.png")
    plt.close()

    # Line chart
    plt.figure(figsize=(6, 4))
    plt.plot(df["steps_taken"], label="Steps Taken", marker="o", color="green", linewidth=2)
    plt.plot(df["enemy_encounters"], label="Enemy Encounters", marker="x", color="red", linewidth=2)

    # Calculate and plot the ratio of steps to enemy encounters
    steps_to_enemy_ratio = df["steps_taken"] / df["enemy_encounters"].replace(0, 1)  # Avoid division by zero
    plt.plot(steps_to_enemy_ratio, label="Steps per Enemy (Balance)", marker="^", color="blue", linestyle="--",
             linewidth=1.5)

    plt.title("Game Balance: Movement vs Enemy Challenge", fontsize=14)
    plt.xlabel("Game Session", fontsize=12)
    plt.ylabel("Count", fontsize=12)
    plt.legend(loc="best")
    plt.grid(True, alpha=0.3)

    # Add annotation about balance
    plt.figtext(0.5, 0.01, "Consistent ratio indicates balanced difficulty level",
                ha="center", fontsize=10, style="italic")

    plt.tight_layout()
    plt.savefig("/Users/ppppphrt/MazeRunner/stat_pic/line_chart_steps_enemy.png")
    plt.close()

