import pygame
from maze import Maze
from player import Player
from constant import CELL_SIZE, ROWS, COLS, WIDTH, HEIGHT, BLACK, BLUE

# Initialize Pygame
pygame.init()
pygame.font.init()  # Ensure fonts are initialized


# Increase window width to add a side panel
PANEL_WIDTH = 200  # Space for UI elements
screen = pygame.display.set_mode((WIDTH + PANEL_WIDTH, HEIGHT))  # Wider screen
pygame.display.set_caption("Maze Runner")

# Create font for displaying messages
font = pygame.font.SysFont('Arial', 24)

# Create Maze and Player
maze = Maze(ROWS, COLS, num_keys=3)  # Specify 3 keys
player = Player()

# Game Loop
running = True
has_won = False
game_message = "Try to escape!"

while running:
    screen.fill(BLACK)

    # Draw maze in its original area
    maze.draw_maze(screen, player.collected_keys, player)

    # Draw Side Panel Background
    pygame.draw.rect(screen, (40, 40, 40), (WIDTH, 0, PANEL_WIDTH, HEIGHT))  # Dark gray sidebar

    # Display keys collected count in the side panel
    keys_text = f"Keys: {len(player.collected_keys)}/{maze.num_keys}"
    keys_surface = font.render(keys_text, True, BLUE)
    screen.blit(keys_surface, (WIDTH + 20, 20))  # Position inside the panel

    # Display game message in the side panel
    if game_message:
        message_surface = font.render(game_message, True, (255, 255, 0))
        screen.blit(message_surface, (WIDTH + 20, 60))  # Message below keys count

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

                # Check if player collects a key
                key_collected = player.check_key_collection(maze)
                if key_collected is not None:
                    game_message = f"Key {key_collected + 1} collected! {maze.num_keys - len(player.collected_keys)} remaining."

                # Check if player reaches the end with all keys
                if player.reached_end(maze.end_pos):
                    if player.has_all_keys(maze):
                        has_won = True
                        game_message = "You've escaped the maze!"
                    else:
                        game_message = f"You need all {maze.num_keys} keys to exit!"

pygame.quit()
