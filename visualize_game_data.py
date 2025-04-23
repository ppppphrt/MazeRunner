from PIL import ImageFont, ImageDraw, Image


def generate_game_stats():
    import pandas as pd
    import matplotlib.pyplot as plt

    df = pd.read_csv("game_results_stat.csv")

    # Create statistical summary table
    plt.figure(figsize=(8, 5))
    plt.axis('off')

    # Calculate key statistics
    stats_data = {
        'Metric': ['Steps Taken', 'Keys Collected', 'Wall Collisions', 'Enemy Encounters', 'Time Taken (s)'],
        'Min': [df['steps_taken'].min(), df['keys_collected'].min(),
                df['wall_collisions'].min(), df['enemy_encounters'].min(), df['time_taken'].min()],
        'Max': [df['steps_taken'].max(), df['keys_collected'].max(),
                df['wall_collisions'].max(), df['enemy_encounters'].max(), df['time_taken'].max()],
        'Average': [df['steps_taken'].mean(), df['keys_collected'].mean(),
                    df['wall_collisions'].mean(), df['enemy_encounters'].mean(), df['time_taken'].mean()],
        'Median': [df['steps_taken'].median(), df['keys_collected'].median(),
                   df['wall_collisions'].median(), df['enemy_encounters'].median(), df['time_taken'].median()],
        'Std Dev': [df['steps_taken'].std(), df['keys_collected'].std(),
                    df['wall_collisions'].std(), df['enemy_encounters'].std(), df['time_taken'].std()]
    }

    # Round numeric values for better display
    for key in stats_data:
        if key != 'Metric':
            stats_data[key] = [round(x, 2) for x in stats_data[key]]

    # Calculate derived metrics
    movement_efficiency = round(df['steps_taken'].sum() / max(df['wall_collisions'].sum(), 1), 2)
    enemy_challenge_ratio = round(df['steps_taken'].sum() / max(df['enemy_encounters'].sum(), 1), 2)
    completion_time_per_key = round(df['time_taken'].mean() / max(df['keys_collected'].mean(), 1), 2)

    # Create the table
    col_labels = list(stats_data.keys())
    cell_text = []
    for i in range(len(stats_data['Metric'])):
        cell_text.append([stats_data[key][i] for key in stats_data.keys()])

    table = plt.table(cellText=cell_text, colLabels=col_labels,
                      loc='center', cellLoc='center',
                      colColours=['#f2f2f2'] * len(col_labels))

    # Style the table
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.scale(1.2, 1.5)

    # Add title
    plt.title('Maze Runner Game Statistics Summary', fontsize=16, pad=20)

    # Add interpretation text below the table
    plt.figtext(0.5, 0.05,
                f"Performance Insights:\n"
                f"• Movement Efficiency: {movement_efficiency} steps per wall collision\n"
                f"• Enemy Challenge Balance: {enemy_challenge_ratio} steps per enemy encounter\n"
                f"• Time Efficiency: {completion_time_per_key} seconds per key collected",
                ha='center', fontsize=10, bbox=dict(facecolor='#f9f9f9', alpha=0.5))

    plt.tight_layout()
    plt.savefig("/Users/ppppphrt/MazeRunner/stat_pic/stats_summary_table.png",
                bbox_inches='tight', dpi=120)
    plt.close()

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

