
import pygame

from GameInfo import GAME_INFO, GameScreen
from objects.Colors import *
from objects.Mouse import MouseButtons

comic_sans_ms = pygame.font.SysFont('Comic Sans MS', 30)

def init_level():
    pass

def render(screen, events, keys, mouse_buttons: MouseButtons):
    if mouse_buttons.left_is_pressed:
        GAME_INFO.NEXT_GAME_SCREEN = GameScreen.GOOD_LEVEL_ONE

    screen.fill(black_color)  # === draw _AFTER_ this line ===

    screen.blit(comic_sans_ms.render("dEVILery", False, evil_red), (0, 0))

    screen.blit(comic_sans_ms.render("Ludum Dare", False, ludum_light_orange), (0, 70))
    screen.blit(comic_sans_ms.render("53", False, ludum_dark_orange), (170, 70))

    screen.blit(comic_sans_ms.render("by L2J2R", False, granny_color), (50, 150))
    screen.blit(comic_sans_ms.render(" • Lou", False, granny_color), (50, 200))
    screen.blit(comic_sans_ms.render(" • Laetitia", False, granny_color), (50, 250))
    screen.blit(comic_sans_ms.render(" • Julien2", False, granny_color), (50, 300))
    screen.blit(comic_sans_ms.render(" • Julien3", False, granny_color), (50, 350))
    screen.blit(comic_sans_ms.render(" • René", False, granny_color), (50, 400))

    screen.blit(comic_sans_ms.render("Click to start", False, yellow_color), (0, 500))
    screen.blit(comic_sans_ms.render("Press [escape] to quit", False, yellow_color), (0, 550))
