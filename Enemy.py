
import random
import pygame
from constant import CELL_SIZE, ROWS, COLS

class Enemy:
    def __init__(self, start_x, start_y, speed=1):
        self.x, self.y = start_x, start_y  # Start position
        self.speed = speed
        self.enemy_encounter = 0  # Number of times the enemy meets the player

    def move_enemy(self, player, maze):
        """Move towards the player while following straight-line movement rules."""
        dx = self.x - player.x
        dy = self.y - player.y

        # Choose horizontal or vertical movement based on distance
        if abs(dx) > abs(dy):  # Move horizontally
            new_x, new_y = self.x - self.speed if dx > 0 else self.x + self.speed, self.y
        else:  # Move vertically
            new_x, new_y = self.x, self.y - self.speed if dy > 0 else self.y + self.speed

        # Ensure the enemy does not move into walls
        if 0 <= new_x < COLS and 0 <= new_y < ROWS and maze[new_y][new_x] == 0:
            self.x, self.y = new_x, new_y

    def detect_player(self, player):
        """Check if the enemy has encountered the player."""
        if self.x == player.x and self.y == player.y:
            self.enemy_encounter += 1
            return True
        return False

    def draw(self, screen):
        """Draw the enemy on the screen."""
        enemy_image = pygame.image.load("enemy.png")  # Load enemy image
        enemy_image = pygame.transform.scale(enemy_image, (CELL_SIZE, CELL_SIZE))
        screen.blit(enemy_image, (self.x * CELL_SIZE, self.y * CELL_SIZE))
