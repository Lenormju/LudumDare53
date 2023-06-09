import pygame

class Thing:
    def __init__(self, rect, speedx, speedy, image):
        self.rect = rect
        self.speedx = speedx
        self.speedy = speedy
        self.DEFAULT_IMAGE_SIZE = (rect.width, rect.height)
        self.image = pygame.image.load(image).convert_alpha()
        self.image = pygame.transform.scale(self.image, self.DEFAULT_IMAGE_SIZE)
    
    def Move(self, x, y):
        self.rect = self.rect.move(x, y)

    def UpdateImage(self, image, width, height):
        self.rect.width = width
        self.rect.height = height
        self.DEFAULT_IMAGE_SIZE = (width, height)
        self.image = pygame.image.load(image).convert_alpha()
        self.image = pygame.transform.scale(self.image, self.DEFAULT_IMAGE_SIZE)
