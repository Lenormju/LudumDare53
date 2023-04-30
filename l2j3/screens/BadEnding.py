
import pygame

from GameInfo import GAME_INFO, GameScreen
from objects.Colors import *
from objects.Mouse import MouseButtons

comic_sans_ms = pygame.font.SysFont('Comic Sans MS', 30)

def init_level():
    pass

def render(screen, events, keys, mouse_buttons: MouseButtons):
    for event in events:
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            GAME_INFO.NEXT_GAME_SCREEN = GameScreen.QUIT

    screen.fill(black_color)  # === draw _AFTER_ this line ===

    screen.blit(comic_sans_ms.render("Nice slaughter :)", False, granny_color), (0, 0))
    screen.blit(comic_sans_ms.render("You sure you are a sane person ?", False, granny_color), (0, 70))
    screen.blit(comic_sans_ms.render("We are a bit concerned", False, granny_color), (0, 140))
    screen.blit(comic_sans_ms.render("You should try to be more kind", False, granny_color), (0, 210))
    screen.blit(comic_sans_ms.render("Hope you enjoyed nonetheless", False, granny_color), (0, 350))
    screen.blit(comic_sans_ms.render("press [escape] to quit", False, yellow_color), (0, 500))
