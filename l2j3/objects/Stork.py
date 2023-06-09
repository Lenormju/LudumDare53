import pygame
from random import *
from objects.Baby import Baby
from objects.Direction import Direction
from objects.Animation import Animation
from objects.DropType import DropType
from GameInfo import GAME_INFO

class Stork:
    IMAGE_SIZE = 50  # carré
    ANIMATION_SPEED = 10

    def __init__(self, images, pos_x=0, pos_y=0):
        self.animation = None
        self.images = images
        self.type = DropType.BABY_TYPE
        self.images_flip = []
        self.baby_picture_path = "assets/baby.png"
        for img in self.images:
            img_copy = img.copy()
            self.images_flip.append(pygame.transform.flip(img_copy, True, False))
        self.current_image = 0
        self.rect = pygame.Rect(pos_x, pos_y, self.IMAGE_SIZE, self.IMAGE_SIZE)
        self.current_direction = Direction.RIGHT
        self.previous_line_y = self.rect.y
        self.has_exited = False

    def Animation(self, screen, flip):
        if flip:
            images = self.images_flip
        else :
            images = self.images
        if self.animation == None or not self.animation.Increment():
            self.animation = Animation(self.ANIMATION_SPEED)
            self.animation.animation = lambda: screen.blit(images[self.current_image], self.rect)
            self.current_image = (self.current_image+1) % len(images)

    def HasExit(self, screen):
        return (not self.rect.colliderect(screen.get_rect())) and self.has_exited

    def Move(self, screen):
        dx, dy = (
            (1, 0) if self.current_direction is Direction.RIGHT
            else (-1, 0) if self.current_direction is Direction.LEFT
            else (0, -1) if self.current_direction is Direction.UP
            else (0, 1) if self.current_direction is Direction.DOWN
            else (None, None)
        )
        # speed up
        k = randint(3,7)
        dx *= k
        dy *= k

        # change direction
        would_exit_on_the_right_side = (self.rect.x + self.IMAGE_SIZE + dx > GAME_INFO.SCREEN_WIDTH)
        would_exit_on_the_left_side = (self.rect.x + dx < 0)
        not_going_down = (self.current_direction is not Direction.DOWN)
        not_going_left = (self.current_direction is not Direction.LEFT)
        not_going_right = (self.current_direction is not Direction.RIGHT)
        is_very_low = (self.rect.y > GAME_INFO.SCREEN_HEIGHT - 250)
        has_gone_down_enough = (self.rect.y + dy > self.previous_line_y + self.IMAGE_SIZE)
        is_on_the_left_side = (self.rect.x < GAME_INFO.SCREEN_WIDTH / 2)
        is_on_the_right_side = (self.rect.x > GAME_INFO.SCREEN_WIDTH / 2)
        
        if would_exit_on_the_right_side and not_going_down and not is_very_low and self.current_direction is Direction.RIGHT:
            self.current_direction = Direction.DOWN
            self.Move(screen)
            return
        elif would_exit_on_the_left_side and not_going_down and not is_very_low and self.current_direction is Direction.LEFT:
            self.current_direction = Direction.DOWN
            self.Move(screen)
            return
        elif not_going_down and (would_exit_on_the_left_side or would_exit_on_the_right_side) and is_very_low and not self.has_exited:
            self.has_exited = True
        elif has_gone_down_enough:
            if is_on_the_right_side and not_going_left:
                self.previous_line_y = self.rect.y
                self.current_direction = Direction.LEFT
                self.Move(screen)
                return
            elif is_on_the_left_side and not_going_right:
                self.previous_line_y = self.rect.y
                self.current_direction = Direction.RIGHT
                self.Move(screen)
                return

        self.rect = self.rect.move(dx, dy)
        has_to_flip = (self.current_direction == Direction.RIGHT)
        self.Animation(screen, has_to_flip )

