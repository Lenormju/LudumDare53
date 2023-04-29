import pygame
pygame.init()

from GameInfo import GAME_INFO, GameScreen

pygame_screen = pygame.display.set_mode((GAME_INFO.SCREEN_WIDTH, GAME_INFO.SCREEN_HEIGHT))

from screens.Title import render as render_screen_title
from screens import GoodLevelOne, GoodEnding, BadInterlude, NeutralEnding

clock = pygame.time.Clock()

keep_running = True
while keep_running:
    GAME_INFO.CURRENT_TICK_NUMBER += 1

    keys = pygame.key.get_pressed() 
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            keep_running = False

    render_function = {
        GameScreen.TITLE: render_screen_title,
        GameScreen.GOOD_LEVEL_ONE: GoodLevelOne.render,
        GameScreen.GOOD_ENDING: GoodEnding.render,
        GameScreen.BAD_INTERLUDE: BadInterlude.render,
        GameScreen.NEUTRAL_ENDING: NeutralEnding.render,
    }.get(GAME_INFO.CURRENT_GAME_SCREEN)
    render_function(pygame_screen, events, keys)

    pygame.display.flip()  # === draw _BEFORE_ this line ===
    clock.tick(GAME_INFO.TARGET_FPS)

    GAME_INFO.CURRENT_GAME_SCREEN = GAME_INFO.NEXT_GAME_SCREEN
    if GAME_INFO.CURRENT_GAME_SCREEN is GameScreen.QUIT:
        keep_running = False

pygame.quit()
