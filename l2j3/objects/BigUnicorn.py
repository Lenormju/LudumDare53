import itertools

import pygame
from random import *
from objects.Baby import Baby
from objects.Direction import Direction
from objects.Animation import Animation
from objects.Sounds import left_turn_sound, right_turn_sound, down_turn_sound
from GameInfo import GAME_INFO
from itertools import cycle


class BigUnicorn:
    IMAGE_SIZE = 40  # carré
    ANIMATION_SPEED = 10

    def __init__(self, images, pos_x=0, pos_y=0):
        self.poops = []
        self.animation = None
        self.images = images
        self.images_flip = []
        for img in self.images:
            img_copy = img.copy()
            self.images_flip.append(pygame.transform.flip(img_copy, True, False))
        self.current_image = 0
        self.rect = pygame.Rect(pos_x, pos_y, self.IMAGE_SIZE, self.IMAGE_SIZE)
        self._move_deltas = itertools.cycle([(3,-1)]*90 + [(3,1)]*90 + [(-3,1)]*90 + [(-3,-1)]*90)
        self._initial_dx = 3

    def HasExit(self, screen):
        return False

    def Animation(self, screen, flip):
        if flip:
            images = self.images_flip
        else:
            images = self.images
        if self.animation == None or not self.animation.Increment():
            self.animation = Animation(self.ANIMATION_SPEED)
            self.animation.animation = lambda: screen.blit(images[self.current_image], self.rect)
            self.current_image = (self.current_image + 1) % len(images)

    def Move(self, screen):
        dx, dy = next(self._move_deltas)
        self.rect = self.rect.move(dx, dy)
        has_to_flip = (dx == self._initial_dx)
        self.Animation(screen, has_to_flip)
