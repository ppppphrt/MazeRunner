import random
import pygame
import sys
import time

import constant
from Enemy import Enemy
from maze import Maze
from player import Player
from Leaderboard import Leaderboard
from constant import CELL_SIZE, ROWS, COLS, WIDTH, HEIGHT, BLACK, BLUE, DARK_BLUE, YELLOW, GRAY, WHITE
from front_page import Button
from GameManager import GameManager

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
font = pygame.font.Font("PixeloidSans-mLxMm.ttf", 20)

# Create Buttons for the menu
start_button = Button("START", SCREEN_WIDTH // 2 - 100, 300, 200, 60, BLUE, DARK_BLUE)
rank_button = Button("RANK", SCREEN_WIDTH // 2 - 100, 400, 200, 60, BLUE, DARK_BLUE)
history = Button("History", SCREEN_WIDTH // 2 - 100, 500, 200, 60, BLUE, DARK_BLUE )

# Input Box for Player Name
input_box = pygame.Rect(SCREEN_WIDTH // 2 - 100, 200, 200, 50)
player_name = ""
active = False
placeholder = "name..."

# Create enemies
enemies = [Enemy(random.randint(0, COLS - 1), random.randint(0, ROWS - 1)) for _ in range(3)]  # 3 enemies

# Initialize Leaderboard
leaderboard = Leaderboard()
game_manager = GameManager()


def show_menu():
    """ Display the main menu and wait for user selection. """
    global player_name, active

    running = True
    while running:
        screen.fill(BLACK)

        # Event handling for input box
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Activate input box if clicked
                if input_box.collidepoint(event.pos):
                    active = True
                else:
                    active = False
            elif event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_BACKSPACE:
                        player_name = player_name[:-1]
                    else:
                        player_name += event.unicode


        # Draw input box
        pygame.draw.rect(screen, (150, 150, 150) if active else (255, 255, 255), input_box, 2)
        # name_surface = font.render(player_name, True, (255, 255, 255))

        # Display text
        if player_name:
            name_surface = font.render(player_name, True, WHITE)
        else:
        # Show placeholder when empty and inactive
            name_surface = font.render(placeholder, True, GRAY)

        screen.blit(name_surface, (input_box.x + 10, input_box.y + 10))

        # Draw buttons
        start_button.draw(screen)
        rank_button.draw(screen)
        history.draw(screen)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if input_box.collidepoint(event.pos):
                    active = True
                else:
                    active = False

                # Check if "Start" is clicked and player entered a name
                if start_button.is_clicked(event) and player_name.strip():
                    return "start"
                elif rank_button.is_clicked(event):
                    return "rank"
            elif event.type == pygame.KEYDOWN and active:
                if event.key == pygame.K_RETURN:
                    if player_name.strip():
                        return "start"
                elif event.key == pygame.K_BACKSPACE:
                    player_name = player_name[:-1]
                else:
                    player_name += event.unicode  # Add typed character


def run_game():
    """ Run the maze game. """
    global player_name  # Ensure we use the name entered
    maze = Maze(ROWS, COLS, num_keys=3)  # Create maze
    player = Player(player_name)  # Pass the name to Player class

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
            enemy.detect_player(player)
            enemy.draw(screen)

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

                    if player.reached_end(maze.end_pos):
                        has_won = True
                        timer_running = False

                        # Check how many keys the player collected
                        if player.collected_keys == maze.num_keys:
                            game_message = f"You've escaped the maze with ALL {player.collected_keys} keys! Bonus awarded!"
                        # elif player.collected_keys > 0:
                        #     game_message = f"You've escaped the maze with {player.collected_keys} keys. Good job!"
                        else:
                            game_message = "You escaped the maze without collecting any keys. Try again for a better score!"

                            # Save score to leaderboard
                            leaderboard.save_score(player.name, len(player.collected_keys), elapsed_time)

                            # Save score to game_results
                            game_manager.save_time(elapsed_time)

                        # else:
                        #     game_message = f"You need all {maze.num_keys} keys to exit!"

    pygame.quit()


# Main Execution
while True:
    choice = show_menu()

    if choice == "start":
        run_game()
    elif choice == "rank":
        print("Show ranking screen (not implemented yet)")  # Placeholder for ranking screen logic
