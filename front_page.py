import pygame
import sys
import constant
# Initialize Pygame
pygame.init()


# Load Pixeloid Font
pygame.font.init()
try:
    font = pygame.font.Font("PixeloidSans-mLxMm.ttf", 40)  # Load Pixeloid font
except:
    print("Font file 'PixeloidSans-mLxMm.ttf' not found!")
    sys.exit()

# Create screen
screen = pygame.display.set_mode((constant.WIDTH, constant.HEIGHT))
pygame.display.set_caption("Maze Runner")

# Button Class
class Button:
    def __init__(self, text, x, y, width, height, color, hover_color):
        self.text = text
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.hover_color = hover_color

    def draw(self, screen):
        mouse_pos = pygame.mouse.get_pos()
        current_color = self.hover_color if self.rect.collidepoint(mouse_pos) else self.color
        pygame.draw.rect(screen, current_color, self.rect, border_radius=10)

        # Render text
        text_surface = font.render(self.text, True, constant.WHITE)
        screen.blit(text_surface, (self.rect.x + (self.rect.width - text_surface.get_width()) // 2,
                                   self.rect.y + (self.rect.height - text_surface.get_height()) // 2))

    def is_clicked(self, event):
        return event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos)

# Create buttons
start_button = Button("START", constant.WIDTH // 2 - 100, 300, 200, 60, constant.BLUE, constant.DARK_BLUE)
rank_button = Button("RANK", constant.WIDTH // 2 - 100, 400, 200, 60, constant.BLUE, constant.DARK_BLUE)

# Main Menu Loop
running = True
while running:
    screen.fill(constant.GRAY)  # Background color

    # Title
    title_surface = font.render("MAZE RUNNER", True, constant.WHITE)
    screen.blit(title_surface, (constant.WIDTH // 2 - title_surface.get_width() // 2, 150))

    # Draw buttons
    start_button.draw(screen)
    rank_button.draw(screen)

    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif start_button.is_clicked(event):
            print("Start Game!")  # Replace this with game start logic
            running = False
        elif rank_button.is_clicked(event):
            print("Show Rankings!")  # Replace this with ranking screen logic

pygame.quit()
