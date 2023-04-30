
import pygame

from GameInfo import GAME_INFO, GameScreen
from objects.Colors import *
from objects.Mouse import MouseButtons, MY_MOUSE_BUTTON_LEFT

comic_sans_ms = pygame.font.SysFont('Comic Sans MS', 30)

def init_level():
    pass

def render(screen, events, keys, mouse_buttons: MouseButtons):
    for event in events:
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == MY_MOUSE_BUTTON_LEFT:
            GAME_INFO.NEXT_GAME_SCREEN = GameScreen.GOOD_LEVEL_TWO

    screen.fill(black_color)  # === draw _AFTER_ this line ===

    screen.blit(comic_sans_ms.render("What an angel you are!", False, sky_color), (0, 0))
    screen.blit(comic_sans_ms.render("Did you know that unicorns         too?", False, sky_color), (0, 70))
    screen.blit(pygame.transform.rotate(comic_sans_ms.render("poop", True, regular_poop_color), 5), (385, 65))

    screen.blit(comic_sans_ms.render("click to continue", False, yellow_color), (0, 500))
