import pygame
from objects.Baby import Baby
from objects.Direction import Direction
from objects.Sounds import left_turn_sound, right_turn_sound, down_turn_sound
from GameInfo import GAME_INFO

class Stork:
    IMAGE_SIZE = 40  # carré

    def __init__(self, image, pos_x=0, pos_y=0):
        self.babies = []
        self.image = image
        self.rect = pygame.Rect(pos_x, pos_y, self.IMAGE_SIZE, self.IMAGE_SIZE)
        self.current_direction = Direction.RIGHT
        self.previous_line_y = self.rect.y

    def DropBaby(self, screen):        
        baby = Baby(self.rect, 1, "assets/baby.png")
        self.babies.append(baby)
        screen.blit(baby.image, baby.rect)
        pygame.mixer.find_channel(force=True).play(down_turn_sound)
        return baby

    def ApplyMoveBaby(self, baby, screen):
        isMoving = baby.GoToDown()
        if isMoving:
            screen.blit(baby.image, baby.rect)
        if not isMoving:
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
        k = 10
        dx *= k
        dy *= k

        # change direction
        if self.rect.x + self.IMAGE_SIZE + dx > GAME_INFO.SCREEN_WIDTH and self.current_direction is not Direction.DOWN:
            self.current_direction = Direction.DOWN
            self.Move(screen)
            return
        elif self.rect.x + dx < 0 and self.current_direction is not Direction.UP:
            self.current_direction = Direction.DOWN
            self.Move(screen)
            return
        elif self.rect.y + dy > self.previous_line_y + self.IMAGE_SIZE:
            if self.rect.x > GAME_INFO.SCREEN_WIDTH / 2:
                if self.current_direction is not Direction.LEFT:
                    self.previous_line_y = self.rect.y
                    self.current_direction = Direction.LEFT
                    self.Move(screen)
                    return
            else:
                if self.current_direction is not Direction.RIGHT:
                    self.previous_line_y = self.rect.y
                    self.current_direction = Direction.RIGHT
                    self.Move(screen)
                    return

        self.rect = self.rect.move(dx, dy)
        screen.blit(self.image, self.rect)

