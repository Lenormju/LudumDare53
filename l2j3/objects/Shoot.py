import pygame
from objects.Thing import Thing

class Shoot(Thing):    
    def GoToUp(self):
        if self.rect.y >= self.speed:
            self.Move(0, -self.speed)
            return True
        if self.rect.y < self.speed:
            return False