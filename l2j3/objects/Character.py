import pygame

class Character:
    def __init__(self, rect, speed, image):
        self.rect = rect
        self.speed = speed
        self.DEFAULT_IMAGE_SIZE = (rect.width, rect.height)
        self.image = pygame.image.load(image).convert()
        self.image = pygame.transform.scale(self.image, self.DEFAULT_IMAGE_SIZE)
    
    def GoToRight(self, xScreen):
        if self.rect.x + self.rect.width < xScreen + self.speed:
            self.Move(self.speed, 0)
    
    def GoToLeft(self):
        if self.rect.x >= self.speed:
            self.Move(-self.speed, 0)

    def Move(self, x, y):
        self.rect = self.rect.move(x, y)
