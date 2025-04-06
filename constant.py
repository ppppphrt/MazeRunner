import pygame

from front_page import Button

CELL_SIZE = 30
ROWS, COLS = 20, 30
WIDTH, HEIGHT = COLS * CELL_SIZE, ROWS * CELL_SIZE

WHITE, BLACK, GREEN, RED, YELLOW, GRAY, BLUE = (
    (255, 255, 255), (0, 0, 0), (0, 255, 0),
    (255, 0, 0), (255, 255, 0), (128, 128, 128), (0, 0, 255)
)

DARK_BLUE = (30, 100, 200)

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

# For LeaderBoard
back_button = Button("BACK", SCREEN_WIDTH // 2 - 100, 500, 200, 60, BLUE, DARK_BLUE )