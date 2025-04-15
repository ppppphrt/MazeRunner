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

    # Line chart
    plt.figure(figsize=(6, 4))
    plt.plot(df["steps_taken"], label="Steps Taken", marker="o", color="green")
    plt.plot(df["enemy_encounters"], label="Enemy Encounters", marker="x", color="red")
    plt.title("Steps and Enemy Encounters Over Sessions")
    plt.xlabel("Game Session")
    plt.ylabel("Count")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("/Users/ppppphrt/MazeRunner/stat_pic/line_chart_steps_enemy.png")
    plt.close()

