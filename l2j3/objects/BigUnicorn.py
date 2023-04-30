import itertools

import pygame
from random import *
from objects.Baby import Baby
from objects.Direction import Direction
from objects.Animation import Animation
from objects.DropType import DropType
from GameInfo import GAME_INFO
from itertools import cycle


class BigUnicorn:
    IMAGE_SIZE = 200  # carré

    def __init__(self, images, animation_speed, pos_x=0, pos_y=0):
        self.poops = []
        self.animation = None
        self.images = []
        self.animation_speed = animation_speed
        for img in images:
            self.images.append(pygame.transform.scale(img, (self.IMAGE_SIZE, self.IMAGE_SIZE)))
        self.current_image = 0
        self.rect = pygame.Rect(pos_x, pos_y, self.IMAGE_SIZE, self.IMAGE_SIZE)
        self._move_deltas = itertools.cycle([(3,-1)]*90 + [(3,1)]*90 + [(-3,1)]*90 + [(-3,-1)]*90)
        self._initial_dx = 3
        self.type = DropType.POOP_TYPE
        self.waiting = False
        self.baby_picture_path = "assets/poop.png"

    def HasExit(self, screen):
        return False

    def Animation(self, screen, flip):
        if self.animation == None or not self.animation.Increment():
            self.animation = Animation(self.animation_speed)
            self.animation.animation = lambda: screen.blit(self.images[self.current_image], self.rect)
            self.current_image = (self.current_image + 1) % len(self.images)

    def Move(self, screen):
        dx, dy = next(self._move_deltas)
        self.rect = self.rect.move(dx, dy)
        has_to_flip = (dx == self._initial_dx)
        self.Animation(screen, has_to_flip)
