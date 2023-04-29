
import pygame

from GameInfo import GAME_INFO, GameScreen
from objects.Colors import *
from objects.Mouse import MouseButtons

comic_sans_ms = pygame.font.SysFont('Comic Sans MS', 30)
comic_sans_ms_small = pygame.font.SysFont('Comic Sans MS', 15)


def render(screen, events, keys, mouse_buttons: MouseButtons):
    for event in events:
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            GAME_INFO.NEXT_GAME_SCREEN = GameScreen.QUIT

    screen.fill(black_color)  # === draw _AFTER_ this line ===

    screen.blit(comic_sans_ms.render("thanks to have played !", False, ludum_light_orange), (0, 0))
    screen.blit(comic_sans_ms.render("your score was :", False, ludum_dark_orange), (0, 50))
    screen.blit(comic_sans_ms.render(str(GAME_INFO.SCORE), False, granny_color), (240, 50))
    screen.blit(comic_sans_ms_small.render("PS: have you tried NOT to catch the babies ?", False, evil_red), (0, 400))
    screen.blit(comic_sans_ms.render("press [escape] to quit", False, yellow_color), (0, 500))
