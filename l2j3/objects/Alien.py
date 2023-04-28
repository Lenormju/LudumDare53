import pygame
from objects.Direction import Direction

class Alien:
    IMAGE_SIZE = 40  # carré
    def __init__(self, image, SCREEN_WIDTH, pos_x=0, pos_y=0):
        self.SCREEN_WIDTH = SCREEN_WIDTH
        self.image = image
        self.rect = pygame.Rect(pos_x, pos_y, self.IMAGE_SIZE, self.IMAGE_SIZE)
        self.current_direction = Direction.RIGHT
        print(self.rect)
        print(self.rect.x, self.rect.y)
        self.previous_line_y = self.rect.y

    def update(self, screen):
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
        if self.rect.x + self.IMAGE_SIZE + dx > self.SCREEN_WIDTH and self.current_direction is not Direction.DOWN:
            print("switching down")
            self.current_direction = Direction.DOWN
            self.update(screen)
            return
        elif self.rect.x + dx < 0 and self.current_direction is not Direction.UP:
            print("switching down")
            self.current_direction = Direction.DOWN
            self.update(screen)
            return
        elif self.rect.y + dy > self.previous_line_y + self.IMAGE_SIZE:
            if self.rect.x > self.SCREEN_WIDTH / 2:
                if self.current_direction is not Direction.LEFT:
                    print("switching left")
                    self.previous_line_y = self.rect.y
                    self.current_direction = Direction.LEFT
                    self.update(screen)
                    return
            else:
                if self.current_direction is not Direction.RIGHT:
                    print("switching right")
                    self.previous_line_y = self.rect.y
                    self.current_direction = Direction.RIGHT
                    self.update(screen)
                    return

        self.rect = self.rect.move(dx, dy)
        screen.blit(self.image, self.rect)

