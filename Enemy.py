import random
import pygame
from constant import CELL_SIZE, ROWS, COLS
from GameManager import  GameManager


class Enemy:
    def __init__(self, maze, player, exit_pos, speed=1, delay_frames=30):
        # Find a valid spawn location
        self.x, self.y = self._get_valid_spawn(maze, player, exit_pos)
        self.speed = speed
        self.enemy_encounter = 0
        self.delay_counter = 0  # Used to delay movement after touching the player
        self.delay_frames = delay_frames  # Frames to pause after encountering player
        self.game_manager = GameManager()

    def _get_valid_spawn(self, maze, player, exit_pos):
        """Spawn the enemy in a walkable location, avoiding player and exit."""
        while True:
            x = random.randint(0, COLS - 1)
            y = random.randint(0, ROWS - 1)

            # Check if maze is a 2D list or a Maze object
            if isinstance(maze, list):
                cell_is_empty = maze[y][x] == 0
            else:  # Assuming it's a Maze object
                cell_is_empty = maze.maze[y][x] == 0

            if (
                    cell_is_empty and
                    (x, y) != (player.x, player.y) and
                    (x, y) != exit_pos
            ):
                return x, y

    def move_enemy(self, player, maze):
        """Move towards the player in straight lines with simple logic."""
        if self.delay_counter > 0:
            self.delay_counter -= 1
            return

        dx = player.x - self.x
        dy = player.y - self.y

        new_x, new_y = self.x, self.y

        # Prefer horizontal or vertical movement
        if abs(dx) > abs(dy):
            new_x = self.x + self.speed if dx > 0 else self.x - self.speed
        else:
            new_y = self.y + self.speed if dy > 0 else self.y - self.speed

        # Check if maze is a 2D list or a Maze object
        if isinstance(maze, list):
            valid_cell = maze[new_y][new_x] == 0 if 0 <= new_x < COLS and 0 <= new_y < ROWS else False
        else:  # Assuming it's a Maze object
            valid_cell = maze.is_valid_move(new_x, new_y)

        # Check bounds and wall collision
        if valid_cell and (new_x, new_y) != (player.x, player.y):
            self.x, self.y = new_x, new_y

    def detect_player(self, player, maze, exit_pos):
        """Check if the enemy has encountered the player."""
        if self.x == player.x and self.y == player.y:
            self.enemy_encounter += 1
            player.respawn()
            self.delay_counter = self.delay_frames  # Pause after encounter
            self.x, self.y = self._get_valid_spawn(maze, player, exit_pos)  # Move enemy
            self.game_manager.record_enemy_encounter()  # Record in GameManager
            return True
        return False

    def draw(self, screen, x_off, y_off):
        """Draw the enemy on the screen."""
        enemy_image = pygame.image.load("pic/enemy.png")
        enemy_image = pygame.transform.scale(enemy_image, (CELL_SIZE, CELL_SIZE))
        screen.blit(enemy_image, (self.x * CELL_SIZE + x_off, self.y * CELL_SIZE + y_off))

    def on_player_caught(self):
        self.game_manager.record_enemy_encounter()
