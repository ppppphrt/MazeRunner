import pygame

from front_page import Button

CELL_SIZE = 30
ROWS, COLS = 19, 29
WIDTH, HEIGHT = COLS * CELL_SIZE, ROWS * CELL_SIZE

WHITE, BLACK, GREEN, RED, YELLOW, GRAY, BLUE = (
    (255, 255, 255), (0, 0, 0), (0, 255, 0),
    (255, 0, 0), (255, 255, 0), (128, 128, 128), (0, 0, 255)
)

DARK_BLUE = (30, 100, 200)

# Constants
PANEL_WIDTH = 600  # Space for UI elements
PANEL_HEIGHT = 700  # Space for UI elements
SCREEN_WIDTH = 1400#WIDTH + (CELL_SIZE*2) + PANEL_WIDTH
SCREEN_HEIGHT = 700 #HEIGHT + (CELL_SIZE*2)
OFF_X = 30
OFF_Y = 60
PANEL_X = OFF_X + (COLS * CELL_SIZE) + OFF_X
PANEL_Y = 0


# Create screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Maze Runner")

# Create font
font = pygame.font.Font("PixeloidSans-mLxMm.ttf", 20)

# Create Buttons for the menu
start_button = Button("START", SCREEN_WIDTH // 2 - 100, 300, 200, 60, BLUE, DARK_BLUE)
rank_button = Button("RANK", SCREEN_WIDTH // 2 - 100, 400, 200, 60, BLUE, DARK_BLUE)
data_button = Button("GAME STAT", SCREEN_WIDTH // 2 - 100, 500, 200, 60, BLUE, DARK_BLUE )

# For LeaderBoard
back_button = Button("BACK", SCREEN_WIDTH // 2 - 100, 500, 200, 60, BLUE, DARK_BLUE )