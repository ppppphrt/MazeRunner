import pygame
from maze import Maze
from player import Player
from constant import CELL_SIZE, ROWS, COLS, WIDTH, HEIGHT, BLACK

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Maze Runner")

# Create Maze and Player
maze = Maze(ROWS, COLS)  # Pass required parameters
player = Player()

# Get maze data
maze_data = maze.generate_maze_backtracking()
key_pos = maze.place_random_item(1)[0]  # Place a single key
# obstacles = maze.place_random_item(10)  # Place obstacles

# Game Loop
running = True
while running:
    screen.fill(BLACK)
    maze.draw_maze(screen, key_pos, player)  # Call draw from Maze class
    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                player.move(0, -1, maze_data)
            elif event.key == pygame.K_DOWN:
                player.move(0, 1, maze_data)
            elif event.key == pygame.K_LEFT:
                player.move(-1, 0, maze_data)
            elif event.key == pygame.K_RIGHT:
                player.move(1, 0, maze_data)

        # Check if player collects the key
        if key_pos is not None and player.collect_key(key_pos):
            key_pos = None

pygame.quit()
