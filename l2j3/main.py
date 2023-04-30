import pygame
pygame.init()

from GameInfo import GAME_INFO, GameScreen

pygame_screen = pygame.display.set_mode((GAME_INFO.SCREEN_WIDTH, GAME_INFO.SCREEN_HEIGHT))

from objects.Mouse import MouseButtons
from screens import Title, GoodLevelOne, GoodLevelTwo, GoodLevelThree, GoodEnding, BadInterlude, BadLevelOne, \
    BadLevelTwo, BadLevelThree, BadEnding, NeutralEnding

clock = pygame.time.Clock()
pygame.mouse.set_visible(False)
pygame.event.set_grab(True)

keep_running = True
while keep_running:
    GAME_INFO.CURRENT_TICK_NUMBER += 1

    mouse_buttons = MouseButtons(*pygame.mouse.get_pressed())
    keys = pygame.key.get_pressed()
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            keep_running = False

    render_function = {
        GameScreen.TITLE: Title.render,
        GameScreen.GOOD_LEVEL_ONE: GoodLevelOne.render,
        GameScreen.GOOD_LEVEL_TWO: GoodLevelTwo.render,
        GameScreen.GOOD_LEVEL_THREE: GoodLevelThree.render,
        GameScreen.GOOD_ENDING: GoodEnding.render,
        GameScreen.BAD_INTERLUDE: BadInterlude.render,
        GameScreen.BAD_LEVEL_ONE: BadLevelOne.render,
        GameScreen.BAD_LEVEL_TWO: BadLevelTwo.render,
        GameScreen.BAD_LEVEL_THREE: BadLevelThree.render,
        GameScreen.NEUTRAL_ENDING: NeutralEnding.render,
        GameScreen.BAD_ENDING: BadEnding.render,
    }.get(GAME_INFO.CURRENT_GAME_SCREEN)
    render_function(pygame_screen, events, keys, mouse_buttons)

    pygame.display.flip()  # === draw _BEFORE_ this line ===
    clock.tick(GAME_INFO.TARGET_FPS)

    GAME_INFO.CURRENT_GAME_SCREEN = GAME_INFO.NEXT_GAME_SCREEN
    if GAME_INFO.CURRENT_GAME_SCREEN is GameScreen.QUIT:
        keep_running = False

pygame.quit()
