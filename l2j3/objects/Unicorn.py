import pygame
from random import *
from objects.Baby import Baby
from objects.Direction import Direction
from objects.Animation import Animation
from objects.DropType import DropType
from GameInfo import GAME_INFO

class Unicorn:
    IMAGE_SIZE = 60  # carré
    ANIMATION_SPEED = 10

    def __init__(self, images, direction, pos_x=0, pos_y=0, delay=0):
        self.animation = None
        self.baby_picture_path = "assets/poop.png" 
        self.type = DropType.POOP_TYPE
        self.current_image = 0
        self.images = []
        self.images_flip = []
        for img in images:
            rescaled_img = pygame.transform.scale(img, (self.IMAGE_SIZE,self.IMAGE_SIZE))
            self.images.append(rescaled_img)
            self.images_flip.append(pygame.transform.flip(rescaled_img, True, False))
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

    def Animation(self, screen, flip):
        if flip:
            images = self.images_flip
        else :
            images = self.images
        if self.animation == None or not self.animation.Increment():
            self.animation = Animation(self.ANIMATION_SPEED)
            self.animation.animation = lambda: screen.blit(images[self.current_image], self.rect)
            self.current_image = (self.current_image+1) % len(images)

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
        has_to_flip = (self.current_direction == Direction.RIGHT)
        self.Animation(screen, has_to_flip )

