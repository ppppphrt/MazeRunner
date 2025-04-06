
import sys
import time

from Enemy import Enemy
from end_screen import show_end_page
from maze import Maze
from player import Player
from Leaderboard import Leaderboard
from constant import *
from GameManager import GameManager

# Initialize Pygame
pygame.init()
pygame.font.init()  # Ensure fonts are initialized

# Input Box for Player Name
input_box = pygame.Rect(SCREEN_WIDTH // 2 - 100, 200, 200, 50)
player_name = ""
active = False
placeholder = "name..."

# Create enemies

maze = Maze(ROWS, COLS, num_keys=3)  # Create maze
player = Player(player_name)  # Pass the name to Player class
exit_pos = (COLS - 1, ROWS - 1)  # Bottom-right as exit
enemies = [Enemy(maze.maze, player, exit_pos) for _ in range(3)]

# Initialize Leaderboard
leaderboard = Leaderboard()
show_leaderboard = False
game_manager = GameManager()
game_state = "menu"

def show_menu():
    """ Display the main menu and wait for user selection. """
    global player_name, active, show_leaderboard, game_state

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

        if game_state == "leaderboard":
            screen.fill((0, 0, 0))  # clear screen
            top_scores = leaderboard.get_top_scores()
            y_offset = 80

            title_text = font.render(" Top 5 Players ", True, (255, 215, 0))
            screen.blit(title_text, (screen.get_width() // 2 - title_text.get_width() // 2, y_offset))
            y_offset += 50

            for i, row in enumerate(top_scores, 1):
                entry = f"{i}. {row[0]} - Score: {row[1]} - Time: {row[2]}s"
                entry_text = font.render(entry, True, (255, 255, 255))
                screen.blit(entry_text, (100, y_offset))
                y_offset += 40

            # button to return to menu
            back_button.draw(screen)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if input_box.collidepoint(event.pos):
                    active = True
                elif back_button.rect.collidepoint(event.pos):
                    game_state = "menu"
                elif rank_button.rect.collidepoint(event.pos):
                    game_state = "leaderboard"

                else:
                    active = False

                # Check if "Start" is clicked and player entered a name
                if start_button.is_clicked(event) and player_name.strip():
                    return "start"

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


        for enemy in enemies:
            if enemy.detect_player(player):  # Check if enemy touches player first
                continue  # Skip movement if it just encountered the player

            enemy.move_enemy(player, maze.maze)  # Move towards player
            enemy.draw(screen)  # Draw enemy

        # Draw Side Panel
        pygame.draw.rect(screen, (40, 40, 40), (WIDTH + 300 , 0, 200, HEIGHT))  # Dark gray sidebar

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
                            game_message = f"You've escaped the maze with {player.collected_keys} keys!"

                        else:
                            game_message = "You escaped the maze without collecting any keys. Try again for a better score!"

                            # Save score to leaderboard
                            leaderboard.save_score(player.name, len(player.collected_keys), elapsed_time)

                            # Save score to game_results
                            game_manager.save_time(elapsed_time)

                            pygame.time.delay(1500)

                            choice = show_end_page()  # Show Restart/Quit screen

                            if choice == "restart":
                                run_game()
                            elif choice == "rank":
                                leaderboard.get_top_scores()

                            elif choice == "quit":
                                pygame.quit()
                                sys.exit()


# Main Execution
while True:
    choice = show_menu()

    if choice == "start":
        run_game()
    elif choice == "rank":
        leaderboard.get_top_scores()  # Placeholder for ranking screen logic
