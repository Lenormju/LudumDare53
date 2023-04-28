import enum

import pygame
from enum import Enum
from objects.Character import Character
from objects.Alien import Alien

# pygame setup
pygame.init()
clock = pygame.time.Clock()
running = True

SCREEN_WIDTH, SCREEN_HEIGHT = 600, 800
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

alien_image1 = pygame.image.load("assets/alien.png")
alien1 = Alien(alien_image1, SCREEN_WIDTH, 0, 0)

current_tick_number = 0
TARGET_FPS = 60

black = (0, 0, 0)

#musique de fond
pygame.mixer.init()
pygame.mixer.music.load('sound/AMBForst_Foret (ID 0100)_LS.wav')
pygame.mixer.music.play()
# get the size for the screen
xScreen, yScreen = screen.get_size()

# Set the character
character = Character(pygame.Rect(xScreen/2, yScreen-100, 100, 100), 10, "assets/kaizen.png")

while running:
    current_tick_number += 1
    if current_tick_number % TARGET_FPS == 0:
        current_tick_number = 0
        print(current_tick_number)
        #son des gentils
        pygame.mixer.Channel(0).play(pygame.mixer.Sound('sound\LASRGun_Blaster star wars 3 (ID 1759)_LS.wav'))
        #son des mechants
        pygame.mixer.Channel(1).play(pygame.mixer.Sound('sound\WEAPWhip_Fouet 4 (ID 2952)_LS.wav'))

    keys = pygame.key.get_pressed() 
    if keys[pygame.K_DOWN]: 
            print ("DOWN") 
    if keys[pygame.K_UP]: 
            print ("UP") 
    if keys[pygame.K_LEFT]:
            character.GoToLeft()
    if keys[pygame.K_RIGHT]:
            character.GoToRight(xScreen)
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(black)  # === draw _AFTER_ this line ===
    alien1.update(screen)
    screen.blit(character.image, (character.rect.x, character.rect.y))

    # flip() the display to put your work on screen
    pygame.display.flip()  # === draw _BEFORE_ this line ===
    clock.tick(TARGET_FPS)

pygame.quit()
