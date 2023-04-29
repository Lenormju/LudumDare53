import pygame
from random import *
from objects.Baby import Baby
from objects.Direction import Direction
from objects.Animation import Animation
from objects.Sounds import left_turn_sound, right_turn_sound, down_turn_sound
from GameInfo import GAME_INFO

class Unicorn:
    IMAGE_SIZE = 40  # carré
    ANIMATION_SPEED = 10

    def __init__(self, image, direction, pos_x=0, pos_y=0):
        self.shits = []
        if direction == Direction.RIGHT:
            image = pygame.transform.flip(image, True, False)
        self.image = image
        self.rect = pygame.Rect(pos_x, pos_y, self.IMAGE_SIZE, self.IMAGE_SIZE)
        self.current_direction = direction
        self.previous_line_y = self.rect.y

    def HasExit(self, screen):
        return not self.rect.colliderect(screen.get_rect())

    def Move(self, screen):
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

