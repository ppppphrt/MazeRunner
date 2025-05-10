import sys
import pygame
from constant import *
from Button import Button, font

def show_instruction_page():
    go_button = Button("GO", SCREEN_WIDTH // 2 - 100, 500, 200, 60, BLUE, DARK_BLUE)

    rules = [
        "1. Use arrow keys (← ↑ → ↓) to move your player.",
        "2. Avoid enemies chasing you in the maze.",
        "3. If you can't avoid enemies, you just have to die and go back to the start point.",
        "4. Reach the maze exit with all keys to win the game.",
        "5. The faster you escape, the higher your score."
    ]

    running = True
    while running:
        screen.fill(BLACK)

        # Title text
        title_surface = font.render("How To Win", True, WHITE)
        screen.blit(title_surface, (SCREEN_WIDTH // 2 - title_surface.get_width() // 2, 100))

        # Render rules
        for idx, rule in enumerate(rules):
            rule_surface = font.render(rule, True, WHITE)
            screen.blit(rule_surface, (100, 180 + idx * 50))  # Adjust Y position for spacing

        go_button.draw(screen)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if back_button.is_clicked(event):
                    return "go"
