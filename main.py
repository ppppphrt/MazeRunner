import random

import pygame
import sys

from Enemy import Enemy
from maze import Maze
from player import Player
from constant import CELL_SIZE, ROWS, COLS, WIDTH, HEIGHT, BLACK, BLUE, DARK_BLUE , YELLOW
from front_page import Button
import time

# Initialize Pygame
pygame.init()
pygame.font.init()  # Ensure fonts are initialized

# Constants
PANEL_WIDTH = 200  # Space for UI elements
SCREEN_WIDTH = WIDTH + PANEL_WIDTH
SCREEN_HEIGHT = HEIGHT

# Create screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Maze Runner")

# Create font
font = pygame.font.SysFont('PixeloidSans-mLxMm.ttf', 20)

# Create Buttons for the menu
start_button = Button("START", SCREEN_WIDTH // 2 - 100, 300, 200, 60, BLUE, DARK_BLUE)
rank_button = Button("RANK", SCREEN_WIDTH // 2 - 100, 400, 200, 60, BLUE, DARK_BLUE)

# create enemies
enemies = [Enemy(random.randint(0, COLS - 1), random.randint(0, ROWS - 1)) for _ in range(3)]  # 3 enemies


def show_menu():
    """ Display the main menu and wait for user selection. """
    running = True
    while running:
        screen.fill(BLACK)

        # Draw buttons
        start_button.draw(screen)
        rank_button.draw(screen)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif start_button.is_clicked(event):
                return "start"  # Start game
            elif rank_button.is_clicked(event):
                return "rank"  # Show ranking

def run_game():
    """ Run the maze game. """
    maze = Maze(ROWS, COLS, num_keys=3)  # Create maze
    player = Player()  # Create player

    running = True
    has_won = False
    game_message = "Try to escape!"
    start_time = time.time()
    elapsed_time = 0
    timer_running = True

    while running:
        screen.fill(BLACK)

        # Draw maze
        maze.draw_maze(screen, player.collected_keys, player)

        # Move and draw enemies
        for enemy in enemies:
            enemy.move_enemy(player, maze.maze)
            enemy.draw(screen)

            if enemy.detect_player(player):
                print("Enemy encountered the player!")

        # Draw Side Panel
        pygame.draw.rect(screen, (40, 40, 40), (WIDTH, 0, PANEL_WIDTH, HEIGHT))  # Dark gray sidebar

        # Display game timer
        if timer_running:
            elapsed_time = int(time.time() - start_time)  # Convert to integer seconds
        time_text = f"Time: {elapsed_time} s"
        time_surface = font.render(time_text, True, YELLOW)
        screen.blit(time_surface, (WIDTH + 20, 20))

        # Display keys collected count
        keys_text = f"Keys: {len(player.collected_keys)}/{maze.num_keys}"
        keys_surface = font.render(keys_text, True, YELLOW)
        screen.blit(keys_surface, (WIDTH + 20, 60))

        # Display game message
        if game_message:
            message_surface = font.render(game_message, True, (255, 255, 0))
            screen.blit(message_surface, (WIDTH + 20, 100))

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
                            timer_running = False
                        else:
                            game_message = f"You need all {maze.num_keys} keys to exit!"

    pygame.quit()

# Main Execution
while True:
    choice = show_menu()

    if choice == "start":
        run_game()
    elif choice == "rank":
        print("Show ranking screen (not implemented yet)")  # Placeholder for ranking screen logic
