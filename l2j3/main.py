import pygame
pygame.init()

from GameInfo import GAME_INFO, GameScreen

pygame_screen = pygame.display.set_mode((GAME_INFO.SCREEN_WIDTH, GAME_INFO.SCREEN_HEIGHT))

from objects.Sounds import background_music_channel
from objects.Mouse import MouseButtons
from screens import Title, GoodLevelOne, GoodLevelTwo, GoodLevelThree, GoodEnding, BadIntro, BadLevelOne, \
    BadLevelTwo, BadLevelThree, BadEnding, NeutralEnding, GoodLevelOneInterlude, GoodLevelTwoInterlude, BadLevelOneInterlude, BadLevelTwoInterlude

clock = pygame.time.Clock()
pygame.mouse.set_visible(False)
pygame.event.set_grab(True)

levels = {
    GameScreen.TITLE: Title,
    GameScreen.GOOD_LEVEL_ONE: GoodLevelOne,
    GameScreen.GOOD_LEVEL_ONE_INTERLUDE: GoodLevelOneInterlude,
    GameScreen.GOOD_LEVEL_TWO: GoodLevelTwo,
    GameScreen.GOOD_LEVEL_TWO_INTERLUDE: GoodLevelTwoInterlude,
    GameScreen.GOOD_LEVEL_THREE: GoodLevelThree,
    GameScreen.GOOD_ENDING: GoodEnding,
    GameScreen.BAD_INTRO: BadIntro,
    GameScreen.BAD_LEVEL_ONE: BadLevelOne,
    GameScreen.BAD_LEVEL_ONE_INTERLUDE: BadLevelOneInterlude,
    GameScreen.BAD_LEVEL_TWO: BadLevelTwo,
    GameScreen.BAD_LEVEL_TWO_INTERLUDE: BadLevelTwoInterlude,
    GameScreen.BAD_LEVEL_THREE: BadLevelThree,
    GameScreen.NEUTRAL_ENDING: NeutralEnding,
    GameScreen.BAD_ENDING: BadEnding,
}

keep_running = True
while keep_running:
    GAME_INFO.CURRENT_TICK_NUMBER += 1

    mouse_buttons = MouseButtons(*pygame.mouse.get_pressed())
    keys = pygame.key.get_pressed()
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            keep_running = False

    if not keep_running:
        continue
    
    levels.get(GAME_INFO.CURRENT_GAME_SCREEN).render(pygame_screen, events, keys, mouse_buttons)

    pygame.display.flip()  # === draw _BEFORE_ this line ===
    clock.tick(GAME_INFO.TARGET_FPS)

    if GAME_INFO.CURRENT_GAME_SCREEN != GAME_INFO.NEXT_GAME_SCREEN:
        GAME_INFO.CURRENT_GAME_SCREEN = GAME_INFO.NEXT_GAME_SCREEN
        background_music_channel.fadeout(1)
        levels.get(GAME_INFO.CURRENT_GAME_SCREEN).init_level()
        GAME_INFO.CUMULATIF_SCORE += GAME_INFO.SCORE
        GAME_INFO.SCORE = 0
    if GAME_INFO.CURRENT_GAME_SCREEN is GameScreen.QUIT:
        keep_running = False

pygame.quit()
