import sys

import pygame

from constant import *
from front_page import Button, font


def show_end_page():
    restart_button = Button("RESTART", SCREEN_WIDTH // 2 - 100, 300, 200, 60, BLUE, DARK_BLUE)
    quit_button = Button("QUIT", SCREEN_WIDTH // 2 - 100, 400, 200, 60, BLUE, DARK_BLUE)

    running = True
    while running:
        screen.fill(BLACK)

        # Show Game Over text
        message_surface = font.render("You've escaped the maze !", True, WHITE)
        screen.blit(message_surface, (SCREEN_WIDTH // 2 - 60, 200))

        restart_button.draw(screen)
        quit_button.draw(screen)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if restart_button.is_clicked(event):
                    return "restart"
                elif quit_button.is_clicked(event):
                    return "quit"


