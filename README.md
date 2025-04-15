# Maze Escape - Pygame 

### Objective
Navigate through the randomly generated maze and reach the exit before time runs out. Avoid obstacles and use strategic movement to escape efficiently.


### Controls
- **Arrow Keys (← ↑ → ↓)** : Move the player in the respective direction.

### Game Mechanics
- **Randomly Generated Mazes** : Each game starts with a unique maze.
- **Straight-Line Enemy Movement** : Enemies move in straight lines, tracking the player based on proximity.
- **Scoring System** : The faster you escape, the higher your score.
- **Traps & Obstacles** : Avoid obstacles that may block your path.
- **Difficulty Levels** : The maze size and enemy count increase with difficulty.

### Winning & Losing
- **Win** : Reach the exit before the timer runs out.
- **Lose** : If an enemy catches you or time runs out, the game ends.

Enjoy the challenge and escape the maze as quickly as possible!



## Installation Instructions

### Prerequisites

- Python 3.7 or later
- pip (Python package installer)

### Setup Steps

1. **Clone the repository**

   ```bash
   git clone https://github.com/ppppphrt/MazeRunner.git
   cd MazeRunner
   ```

2. **Set up a virtual environment (recommended)**

   ```bash
   # On Windows
   python -m venv venv
   venv\Scripts\activate

   # On macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**

   ```bash
   python main.py
   ```






