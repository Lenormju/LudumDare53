
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
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            GAME_INFO.NEXT_GAME_SCREEN = GameScreen.GOOD_LEVEL_ONE
            GAME_INFO.CUMULATIF_SCORE = 0
            GAME_INFO.SCORE = 0

    screen.fill(black_color)  # === draw _AFTER_ this line ===

    screen.blit(comic_sans_ms.render("You will do better next time ...", False, granny_color), (0, 0))
    screen.blit(comic_sans_ms.render("press [escape] to quit", False, yellow_color), (0, 500))
    screen.blit(comic_sans_ms.render("press [space] to restart", False, yellow_color), (0, 550))
