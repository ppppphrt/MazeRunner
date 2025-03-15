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

# # Create screen
# screen = pygame.display.set_mode((constant.WIDTH, constant.HEIGHT))
# pygame.display.set_caption("Maze Runner")

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


