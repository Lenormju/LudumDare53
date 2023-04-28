import pygame
pygame.init()

from GameInfo import GAME_INFO

pygame_screen = pygame.display.set_mode((GAME_INFO.SCREEN_WIDTH, GAME_INFO.SCREEN_HEIGHT))

from screens.Shoot import render as render_screen_shoot

clock = pygame.time.Clock()

keep_running = True
while keep_running:
    GAME_INFO.CURRENT_TICK_NUMBER += 1

    keys = pygame.key.get_pressed() 
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            keep_running = False

    render_screen_shoot(pygame_screen, events, keys)

    pygame.display.flip()  # === draw _BEFORE_ this line ===
    clock.tick(GAME_INFO.TARGET_FPS)

pygame.quit()
