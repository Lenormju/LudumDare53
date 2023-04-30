
import pygame

from GameInfo import GAME_INFO, GameScreen
from objects.Colors import *
from objects.Mouse import MouseButtons

comic_sans_ms = pygame.font.SysFont('Comic Sans MS', 30)

logo = pygame.image.load("assets/logo_devilery.png")

def init_level():
    pass

def render(screen, events, keys, mouse_buttons: MouseButtons):
    if mouse_buttons.left_is_pressed:
        GAME_INFO.NEXT_GAME_SCREEN = GameScreen.GOOD_LEVEL_ONE

    screen.fill(black_color)  # === draw _AFTER_ this line ===

    # screen.blit(comic_sans_ms.render("dEVILery", False, evil_red), (0, 0))
    screen.blit(pygame.transform.scale(logo, (560, 102)), (10, 10))

    screen.blit(comic_sans_ms.render("Ludum Dare", False, ludum_light_orange), (20, 120))
    screen.blit(comic_sans_ms.render("53", False, ludum_dark_orange), (195, 120))

    screen.blit(comic_sans_ms.render("by L2J2R", False, granny_color), (70, 170))
    screen.blit(comic_sans_ms.render(" • Lou", False, granny_color), (100, 220))
    screen.blit(comic_sans_ms.render(" • Laetitia", False, granny_color), (100, 270))
    screen.blit(comic_sans_ms.render(" • Julien2", False, granny_color), (100, 320))
    screen.blit(comic_sans_ms.render(" • Julien3", False, granny_color), (100, 370))
    screen.blit(comic_sans_ms.render(" • René", False, granny_color), (100, 420))

    screen.blit(pygame.transform.rotate(comic_sans_ms.render("Catch", True, sky_color), 15), (370, 200))
    screen.blit(pygame.transform.rotate(comic_sans_ms.render("All", True, sky_color), 15), (400, 235))
    screen.blit(pygame.transform.rotate(comic_sans_ms.render("The", True, sky_color), 15), (400, 265))
    screen.blit(pygame.transform.rotate(comic_sans_ms.render("Babies!", True, sky_color), 15), (390, 285))

    screen.blit(comic_sans_ms.render("Click to start", False, yellow_color), (0, 500))
    screen.blit(comic_sans_ms.render("Press [escape] to quit", False, yellow_color), (0, 550))
