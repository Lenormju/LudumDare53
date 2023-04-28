import pygame
from objects.Thing import Thing
from objects.Sounds import explosion_sound

class Shoot(Thing):    
    def GoToUp(self):
        if self.rect.y >= self.speed:
            self.Move(0, -self.speed)
            return True
        if self.rect.y < self.speed:
            return False
        
    def isCollideEnnemy(self, ennemies):
        for ennemy in ennemies:
            if(ennemy.rect.colliderect(self.rect)):
                pygame.mixer.find_channel(force=True).play(explosion_sound)
                return ennemy
        return None