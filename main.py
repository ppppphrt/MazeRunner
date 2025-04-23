
import sys
import time

from Enemy import Enemy
from end_screen import show_end_page
from maze import Maze
from player import Player
from Leaderboard import Leaderboard
from constant import *
from GameManager import GameManager
from visualize_game_data import generate_game_stats

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
gm = GameManager()
game_state = "menu"

# Show game stat
def load_stat_images():
    time_img = pygame.image.load("stat_pic/time_taken_stat.png")
    bar_chart = pygame.image.load("stat_pic/bar_chart_avg_keys_collisions.png")
    line_chart = pygame.image.load("stat_pic/line_chart_steps_enemy.png")
    stat_summary = pygame.image.load("stat_pic/stats_summary_table.png")
    return bar_chart, line_chart, time_img , stat_summary

show_stats = False
stat_images = []

def show_menu():
    """ Display the main menu and wait for user selection. """
    global player_name, active, show_leaderboard, game_state, show_stats, stat_images

    scroll_offset = 0
    scroll_speed = 30
    max_scroll = 0

    running = True
    while running:
        screen.fill(BLACK)

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if input_box.collidepoint(event.pos):
                    active = True
                else:
                    active = False

                if game_state == "menu":
                    if start_button.is_clicked(event) and player_name.strip():
                        return "start"
                    elif rank_button.rect.collidepoint(event.pos):
                        game_state = "leaderboard"
                    elif data_button.rect.collidepoint(event.pos):
                        game_state = "Game Stat"
                        generate_game_stats()
                        stat_images = load_stat_images()
                        show_stats = True
                        scroll_offset = 0

                        # Calculate max scroll based on images
                        total_height = 100 + sum(img.get_height() + 40 for img in stat_images)
                        visible_height = screen.get_height()
                        max_scroll = max(0, total_height - visible_height)

                elif game_state in ("leaderboard", "Game Stat"):
                    if back_button.rect.collidepoint(event.pos):
                        game_state = "menu"
                        show_stats = False

                if game_state == "Game Stat" and show_stats:
                    if event.button == 4:  # Scroll up
                        scroll_offset = min(scroll_offset + scroll_speed, 0)
                    elif event.button == 5:  # Scroll down
                        scroll_offset = max(scroll_offset - scroll_speed, -max_scroll)

            elif event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_RETURN and player_name.strip():
                        return "start"
                    elif event.key == pygame.K_BACKSPACE:
                        player_name = player_name[:-1]
                    else:
                        player_name += event.unicode
                elif game_state == "Game Stat" and show_stats:
                    if event.key == pygame.K_UP:
                        scroll_offset = min(scroll_offset + scroll_speed, 0)
                    elif event.key == pygame.K_DOWN:
                        scroll_offset = max(scroll_offset - scroll_speed, -max_scroll)

        # --- Render UI ---
        if game_state == "menu":
            pygame.draw.rect(screen, (150, 150, 150) if active else (255, 255, 255), input_box, 2)
            name_surface = font.render(player_name if player_name else placeholder, True, WHITE if player_name else GRAY)
            screen.blit(name_surface, (input_box.x + 10, input_box.y + 10))
            start_button.draw(screen)
            rank_button.draw(screen)
            data_button.draw(screen)

        elif game_state == "leaderboard":
            screen.fill((0, 0, 0))
            top_scores = leaderboard.get_top_scores()
            y_offset = 80
            title_text = font.render(" Top 5 Players ", True, (255, 215, 0))
            screen.blit(title_text, (screen.get_width() // 2 - title_text.get_width() // 2, y_offset))
            y_offset += 50
            for i, row in enumerate(top_scores, 1):
                entry = f"{i}. {row[0]} - Time: {row[2]}s"
                entry_text = font.render(entry, True, (255, 255, 255))
                screen.blit(entry_text, (100, y_offset))
                y_offset += 40
            back_button.draw(screen)

        elif game_state == "Game Stat" and show_stats:
            screen.fill((0, 0, 0))

            # Display each stat image with vertical spacing and scroll offset
            y = 100 + scroll_offset
            for i, img in enumerate(stat_images):
                screen.blit(img, (60, y))
                y += img.get_height() + 40  # 40px spacing

            back_button.draw(screen)

        pygame.display.flip()


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
            if enemy.detect_player(player, maze, exit_pos):  # Check if enemy touches player first
                gm.record_enemy_encounter()
                continue # Skip movement if it just encountered the player


            enemy.move_enemy(player, maze.maze)  # Move towards player
            enemy.draw(screen)  # Draw enemy

        # Draw Side Panel
        pygame.draw.rect(screen, (40, 40, 40), (WIDTH + 300 , 0, 200, HEIGHT))  # Dark gray sidebar

        # Display game timer
        if timer_running:
            elapsed_time = int(time.time() - start_time)  # Convert to integer seconds
            gm.record_time(elapsed_time)
        time_text = f"Time: {elapsed_time} s"
        time_surface = font.render(time_text, True, YELLOW)
        screen.blit(time_surface, (WIDTH + 20, 20))

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
                    gm.record_step()
                # else:
                #     gm.record_wall_collision()

                    # Check if player collects a key
                    key_collected = player.check_key_collection(maze)
                    if key_collected is not None:
                        game_message = (f"{len(player.collected_keys)} Key collected! \n"
                                        f"{maze.num_keys - len(player.collected_keys)} \n"
                                        f"remaining to ESCAPE !")

                    # Check if player reaches the end with all keys
                    if player.reached_end(maze.end_pos):
                        if player.has_all_keys(maze):
                            has_won = True
                            game_message = "You've escaped the maze!"
                            timer_running = False

                            leaderboard.save_score(player.name, len(player.collected_keys), elapsed_time)
                            gm.record_key(len(player.collected_keys))

                            # pygame.time.delay(1500)

                            choice = show_end_page()  # Show Restart/Quit screen

                            gm.save_stats()
                            gm.reset_stats()

                            if choice == "restart":
                                run_game()
                            elif choice == "rank":
                                leaderboard.get_top_scores()

                            elif choice == "quit":
                                pygame.quit()
                                sys.exit()

                            elif choice == "Game Stat":
                                generate_game_stats()
                    else:
                        game_message = "You have to collect ALL KEYS to escape!"
                else:
                    # Handle wall collision
                    gm.record_wall_collision()



# Main Execution
while True:
    choice = show_menu()

    if choice == "start":
        run_game()
    elif choice == "rank":
        leaderboard.get_top_scores()  # Placeholder for ranking screen logic
    elif choice == "Game Stat":
        generate_game_stats()

