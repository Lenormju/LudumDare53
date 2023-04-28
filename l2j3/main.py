# Example file showing a basic pygame "game loop"
import enum

import pygame
from enum import Enum
from objects.Character import Character

# pygame setup
pygame.init()
clock = pygame.time.Clock()
running = True


IMAGE_SIZE = 40  # carré

SCREEN_WIDTH, SCREEN_HEIGHT = 600, 800
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))


class Direction(enum.Enum):
    UP = "up"
    DOWN = "down"
    LEFT = "left"
    RIGHT = "right"


class Alien:
    def __init__(self, image, pos_x=0, pos_y=0):
        self.image = image
        self.rect = pygame.Rect(pos_x, pos_y, IMAGE_SIZE, IMAGE_SIZE)
        self.current_direction = Direction.RIGHT
        print(self.rect)
        print(self.rect.x, self.rect.y)
        self.previous_line_y = self.rect.y

    def update(self):
        dx, dy = (
            (1, 0) if self.current_direction is Direction.RIGHT
            else (-1, 0) if self.current_direction is Direction.LEFT
            else (0, -1) if self.current_direction is Direction.UP
            else (0, 1) if self.current_direction is Direction.DOWN
            else (None, None)
        )
        # speed up
        k = 10
        dx *= k
        dy *= k

        # change direction
        if self.rect.x + IMAGE_SIZE + dx > SCREEN_WIDTH and self.current_direction is not Direction.DOWN:
            print("switching down")
            self.current_direction = Direction.DOWN
            self.update()
            return
        elif self.rect.x + dx < 0 and self.current_direction is not Direction.UP:
            print("switching down")
            self.current_direction = Direction.DOWN
            self.update()
            return
        elif self.rect.y + dy > self.previous_line_y + IMAGE_SIZE:
            if self.rect.x > SCREEN_WIDTH / 2:
                if self.current_direction is not Direction.LEFT:
                    print("switching left")
                    self.previous_line_y = self.rect.y
                    self.current_direction = Direction.LEFT
                    self.update()
                    return
            else:
                if self.current_direction is not Direction.RIGHT:
                    print("switching right")
                    self.previous_line_y = self.rect.y
                    self.current_direction = Direction.RIGHT
                    self.update()
                    return

        self.rect = self.rect.move(dx, dy)
        screen.blit(self.image, self.rect)


alien_image1 = pygame.image.load("assets/alien.png")
alien1 = Alien(alien_image1, 0, 0)


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
character = Character(pygame.Rect(600, 620, 100, 100), 10, "assets/kaizen.png")

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
    alien1.update()
    screen.blit(character.image, (character.rect.x, character.rect.y))

    # flip() the display to put your work on screen
    pygame.display.flip()  # === draw _BEFORE_ this line ===
    clock.tick(TARGET_FPS)

pygame.quit()
