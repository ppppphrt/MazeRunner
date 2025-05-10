
## Overview

**Maze Escape** is a puzzle-adventure game developed with Python’s Pygame library. Players navigate a dynamically generated maze while avoiding obstacles and pursuing enemies. The objective is to collect keys and escape through the exit before time runs out. The game incorporates a timer-based scoring system, rewarding faster completions with higher scores, and a local leaderboard to track top performances.

Key features include:
- Random maze generation using the **Depth-First Search (DFS)** algorithm
- Enemies that track the player using proximity-based distance detection, moving only in straight lines and increasing speed when nearby
- Local leaderboard storage for high scores
- A simple yet strategic gameplay loop with timed scoring and enemy patrols

---

## Concept

### Game Mechanics:
The core gameplay revolves around guiding a player through a maze while evading enemy patrols and collecting keys to unlock the exit. Key mechanics include:
- **Movement**: Arrow keys (← ↑ → ↓)
- **Key Collection**: Required to unlock the maze exit
- **Enemy Behavior**: Enemies track the player when nearby, moving in straight lines. They speed up when within a specific proximity.
- **Scoring**: Based on the time taken to escape

## UML Class Diagram
![diagram](https://github.com/user-attachments/assets/a70227d8-f7f6-47ee-98d6-28ecb68b0df2)
