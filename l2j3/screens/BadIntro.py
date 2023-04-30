
import pygame

from GameInfo import GAME_INFO, GameScreen
from objects.Colors import *
from objects.Mouse import MouseButtons

comic_sans_ms = pygame.font.SysFont('Comic Sans MS', 30)

def init_level():
    pass

def render(screen, events, keys, mouse_buttons: MouseButtons):
    if mouse_buttons.left_is_pressed:
        GAME_INFO.NEXT_GAME_SCREEN = GameScreen.BAD_LEVEL_ONE

    screen.fill(black_color)  # === draw _AFTER_ this line ===

    screen.blit(comic_sans_ms.render("You sure missed a lot of them !", False, evil_red), (0, 0))
    screen.blit(comic_sans_ms.render("Are you intentionally clumsy ?", False, evil_red), (0, 70))
    screen.blit(comic_sans_ms.render("Lets find out ...", False, evil_red), (0, 140))
    screen.blit(pygame.transform.rotate(comic_sans_ms.render("WITH A GUN !!!", True, evil_red), 10), (0, 250))
    screen.blit(comic_sans_ms.render("click to start gunning", False, yellow_color), (0, 500))
