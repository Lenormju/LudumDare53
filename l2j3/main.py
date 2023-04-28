# Example file showing a basic pygame "game loop"
import enum

import pygame
from enum import Enum

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

    def update(self):
        dx, dy = (
            (1, 0) if self.current_direction is Direction.RIGHT
            else (-1, 0) if self.current_direction is Direction.LEFT
            else (0, -1) if self.current_direction is Direction.UP
            else (0, 1) if self.current_direction is Direction.DOWN
            else (None, None)
        )
        # change direction
        if self.rect.x + IMAGE_SIZE + dx > SCREEN_WIDTH + 5:
            print("switching down")
            self.current_direction = Direction.DOWN
        elif self.rect.x - dx < -5:
            print("switching up")
            self.current_direction = Direction.UP
        elif self.rect.y + IMAGE_SIZE + dy > SCREEN_HEIGHT + 5:
            print("switching left")
            self.current_direction = Direction.LEFT
        elif self.rect.y - dy < -5:
            print("switching right")
            self.current_direction = Direction.RIGHT
        # speed up
        k = 5
        dx *= k
        dy *= k
        self.rect = self.rect.move(dx, dy)
        screen.blit(self.image, self.rect)


alien_image1 = pygame.image.load("assets/alien.png")
alien1 = Alien(alien_image1, 0, 0)


current_tick_number = 0
TARGET_FPS = 60

black = (0, 0, 0)


while running:
    current_tick_number += 1
    if current_tick_number % TARGET_FPS == 0:
        current_tick_number = 0
        print(current_tick_number)


    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(black)  # === draw _AFTER_ this line ===
    alien1.update()
    print(alien1.rect)

    # flip() the display to put your work on screen
    pygame.display.flip()  # === draw _BEFORE_ this line ===
    clock.tick(TARGET_FPS)

pygame.quit()
