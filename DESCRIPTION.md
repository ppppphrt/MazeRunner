
## Overview

**Maze Escape** is a puzzle-adventure game developed with Python’s Pygame library. Players navigate a dynamically generated maze while avoiding obstacles and pursuing enemies. The objective is to collect keys and escape through the exit before time runs out. The game incorporates a timer-based scoring system, rewarding faster completions with higher scores, and a local leaderboard to track top performances.

Key features include:
- Random maze generation using the **Prim** algorithm
- Enemies that track the player using proximity-based distance detection, moving only in straight lines and and try to chasing player when nearby
- A simple yet strategic gameplay loop with timed scoring.

---

## Concept

### Game Mechanics:
The core gameplay revolves around guiding a player through a maze while evading enemy patrols and collecting keys to unlock the exit. Key mechanics include:
- **Movement**: Arrow keys (← ↑ → ↓)
- **Key Collection**: Required ALL keys to unlock the maze exit
- **Enemy Behavior**: Enemies track the player when nearby, moving in straight lines.
- **Scoring**: Based on the time taken to escape

## UML Class Diagram
![updated_diagram](https://github.com/user-attachments/assets/93833de7-b028-46e9-8f05-1a470151fa2b)

[Youtube Link](https://youtu.be/dtZ33MDoJm0)
