import pygame
from random import *
from objects.Baby import Baby
from objects.Direction import Direction
from objects.Animation import Animation
from objects.DropType import DropType
from objects.Sounds import left_turn_sound, right_turn_sound, down_turn_sound
from GameInfo import GAME_INFO

class Unicorn:
    IMAGE_SIZE = 60  # carré
    ANIMATION_SPEED = 10

    def __init__(self, image, direction, pos_x=0, pos_y=0, delay=0):
        self.baby_picture_path = "assets/poop.png" 
        self.type = DropType.POOP_TYPE
        image = pygame.transform.scale(image, (self.IMAGE_SIZE,self.IMAGE_SIZE))
        if direction == Direction.RIGHT:
            image = pygame.transform.flip(image, True, False)
        self.image = image
        self.rect = pygame.Rect(pos_x, pos_y, self.IMAGE_SIZE, self.IMAGE_SIZE)
        self.current_direction = direction
        self.previous_line_y = self.rect.y
        self.delay = delay
        self.currentTick = 0
        self.waiting = True

    def HasExit(self, screen):
        if self.currentTick < self.delay:
            return False
        return not self.rect.colliderect(screen.get_rect())

    def Move(self, screen):
        self.currentTick += 1
        if self.currentTick < self.delay:
            return
        self.waiting = False
        dx, dy = (
            (1, 0) if self.current_direction is Direction.RIGHT
            else (-1, 0) if self.current_direction is Direction.LEFT
            else (None, None)
        )
        # speed up
        k = randint(2,5)
        dx *= k
        dy *= k
            
        self.rect = self.rect.move(dx, dy)
        screen.blit(self.image, self.rect)

