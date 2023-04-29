import pygame
from objects.Baby import Baby
from objects.Direction import Direction
from objects.Animation import Animation
from objects.Sounds import left_turn_sound, right_turn_sound, down_turn_sound
from GameInfo import GAME_INFO

class Stork:
    IMAGE_SIZE = 40  # carré
    ANIMATION_SPEED = 10

    def __init__(self, images, pos_x=0, pos_y=0):
        self.babies = []
        self.animation = None
        self.images = images
        self.current_image = 0
        self.rect = pygame.Rect(pos_x, pos_y, self.IMAGE_SIZE, self.IMAGE_SIZE)
        self.current_direction = Direction.RIGHT
        self.previous_line_y = self.rect.y

    def DropBaby(self, screen):        
        baby = Baby(self.rect, 5, "assets/baby.png")
        self.babies.append(baby)
        screen.blit(baby.image, baby.rect)
        pygame.mixer.find_channel(force=True).play(down_turn_sound)
        return baby

    def isCollideBabies(self, character):
        for baby in self.babies:
            if(baby.rect.colliderect(character.rect)):
                GAME_INFO.SCORE += 1
                self.babies.remove(baby)
    
    def ApplyMoveBaby(self, baby, screen):
        isMoving = baby.GoToDown()
        if isMoving:
            screen.blit(baby.image, baby.rect)
        if not isMoving:
            GAME_INFO.SCORE -= 1
            self.babies.remove(baby)

    def Move(self, screen):
        dx, dy = (
            (1, 0) if self.current_direction is Direction.RIGHT
            else (-1, 0) if self.current_direction is Direction.LEFT
            else (0, -1) if self.current_direction is Direction.UP
            else (0, 1) if self.current_direction is Direction.DOWN
            else (None, None)
        )
        # speed up
        k = 5
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

        if would_exit_on_the_right_side and not_going_down and not is_very_low:
            self.current_direction = Direction.DOWN
            self.Move(screen)
            return
        elif would_exit_on_the_left_side and not_going_down and not is_very_low:
            self.current_direction = Direction.DOWN
            self.Move(screen)
            return
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
        if self.animation == None:
            self.animation = Animation(self.ANIMATION_SPEED)
            self.animation.animation = lambda: screen.blit(self.images[self.current_image], self.rect)
            self.current_image = (self.current_image+1) % len(self.images)
        if not self.animation.Increment():
            self.animation = None

