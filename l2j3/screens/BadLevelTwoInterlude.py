
import pygame

from GameInfo import GAME_INFO, GameScreen
from objects.Colors import *
from objects.Mouse import MouseButtons, MY_MOUSE_BUTTON_LEFT

comic_sans_ms = pygame.font.SysFont('Comic Sans MS', 30)


def render(screen, events, keys, mouse_buttons: MouseButtons):
    for event in events:
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == MY_MOUSE_BUTTON_LEFT:
            GAME_INFO.NEXT_GAME_SCREEN = GameScreen.BAD_LEVEL_THREE

    screen.fill(black_color)  # === draw _AFTER_ this line ===

    screen.blit(comic_sans_ms.render("And still more coming!", False, evil_red), (0, 0))
    screen.blit(comic_sans_ms.render("You seem to have awaken their boss :O", False, evil_red), (0, 70))

    screen.blit(comic_sans_ms.render("click to continue", False, yellow_color), (0, 500))
