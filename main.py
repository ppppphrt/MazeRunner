import pygame
from maze import Maze
from player import Player
from constant import CELL_SIZE, ROWS, COLS, WIDTH, HEIGHT, BLACK

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Maze Runner")

# Create Maze and Player
maze = Maze(ROWS, COLS)
player = Player()

# Get maze data
key_pos = maze.place_random_item(1)[0] if maze.place_random_item(1) else None
# End position is now a property of the maze object
end_pos = maze.end_pos

# Game Loop
running = True
has_won = False
while running:
    screen.fill(BLACK)

    # Draw maze and components (now includes drawing the end position)
    maze.draw_maze(screen, key_pos if not player.has_key else None, player)

    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN and not has_won:
            new_x, new_y = player.x, player.y

            if event.key == pygame.K_UP:
                new_y -= 1
            elif event.key == pygame.K_DOWN:
                new_y += 1
            elif event.key == pygame.K_LEFT:
                new_x -= 1
            elif event.key == pygame.K_RIGHT:
                new_x += 1

            # Check if move is valid
            if maze.is_valid_move(new_x, new_y):
                player.x, player.y = new_x, new_y

                # Check if player collects the key
                if key_pos is not None and (player.x, player.y) == key_pos:
                    player.has_key = True
                    key_pos = None

                # Check if player reaches the end with the key
                if (player.x, player.y) == end_pos and player.has_key:
                    has_won = True
                    print("You've won!")

pygame.quit()