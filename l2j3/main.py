import pygame
from objects.Character import Character
from objects.Alien import Alien
from objects.Sounds import background_sound, explosion_sound

# pygame setup
pygame.init()
clock = pygame.time.Clock()
running = True
pygame.font.init()

SCREEN_WIDTH, SCREEN_HEIGHT = 600, 400
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

my_font = pygame.font.SysFont('Comic Sans MS', 30)

alien_image1 = pygame.image.load("assets/alien.png")
ennemies = []
ennemies.append(Alien(alien_image1, SCREEN_WIDTH, 0, 0))
ennemies.append(Alien(alien_image1, SCREEN_WIDTH, 120, 0))
ennemies.append(Alien(alien_image1, SCREEN_WIDTH, 300, 0))

current_tick_number = 0
TARGET_FPS = 60

black = (0, 0, 0)

background_sound.play(loops=-1)

# get the size for the screen
xScreen, yScreen = screen.get_size()

# Set the character
character = Character(pygame.Rect(xScreen/2, yScreen-100, 100, 100), 10, "assets/kaizen.png")

player_has_lost = False

while running:
    shooting = False
    current_tick_number += 1
    if current_tick_number % TARGET_FPS == 0:
        current_tick_number = 0

    keys = pygame.key.get_pressed() 
    if keys[pygame.K_LEFT]:
        character.GoToLeft()
    if keys[pygame.K_RIGHT]:
        character.GoToRight(xScreen)
        
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                shooting = True

    screen.fill(black)  # === draw _AFTER_ this line ===
    for ennemy in ennemies:
        ennemy.update(screen)
    if shooting:
        character.DoShoot(screen)
        
    for ennemy in character.ApplyShoots(screen, ennemies):
        ennemies.remove(ennemy)

    # check if alien destroys the player
    for ennemy in ennemies:
        if ennemy.rect.colliderect(character.rect):
            explosion_sound.play()
            player_has_lost = True
            break

    if player_has_lost:
        character.rect = pygame.Rect(5000, 5000, 0, 0)  # out of sight !
        red_color = (255, 0, 0)
        text_surface = my_font.render('You have lost!', False, red_color)
        screen.blit(text_surface, (0, 0))
    else:
        screen.blit(character.image, character.rect)


    # flip() the display to put your work on screen
    pygame.display.flip()  # === draw _BEFORE_ this line ===
    clock.tick(TARGET_FPS)

pygame.quit()
