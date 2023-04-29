
import pygame

from GameInfo import GAME_INFO, GameScreen
from objects.Colors import *

comic_sans_ms = pygame.font.SysFont('Comic Sans MS', 30)


def render(screen, events, keys):
    for event in events:
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            GAME_INFO.NEXT_GAME_SCREEN = GameScreen.QUIT

    screen.fill(black_color)  # === draw _AFTER_ this line ===

    screen.blit(comic_sans_ms.render("You will do better next time ...", False, granny_color), (0, 0))
    screen.blit(comic_sans_ms.render("press [escape] to quit", False, yellow_color), (0, 500))
