
import pygame

from GameInfo import GAME_INFO, GameScreen
from objects.Colors import *

comic_sans_ms = pygame.font.SysFont('Comic Sans MS', 30)


def render(screen, events, keys):
    for event in events:
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            GAME_INFO.NEXT_GAME_SCREEN = GameScreen.QUIT

    screen.fill(black_color)  # === draw _AFTER_ this line ===

    screen.blit(comic_sans_ms.render("You sure missed a lot of them !", False, evil_red), (0, 0))
    screen.blit(comic_sans_ms.render("Are you intentionally clumsy ?", False, evil_red), (0, 70))
    screen.blit(comic_sans_ms.render("Lets find out ...", False, evil_red), (0, 140))
    screen.blit(comic_sans_ms.render("WITH A GUN !!!", False, evil_red), (0, 250))
    screen.blit(comic_sans_ms.render("press [enter] to start gunning", False, yellow_color), (0, 500))
