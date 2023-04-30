import pygame
from objects.Thing import Thing
from objects.Sounds import explosion_sound, play_sound
from GameInfo import GAME_INFO

class Shoot(Thing):    
    def GoToUp(self):
        if self.rect.y >= self.speedy:
            self.Move(self.speedx, -self.speedy)
            return True
        if self.rect.y < self.speedy:
            return False
        
    def isCollideEnnemy(self, ennemies):
        for ennemy in ennemies:
            if(ennemy.rect.colliderect(self.rect)):
                GAME_INFO.SCORE += 1
                play_sound(explosion_sound)
                return ennemy
        return None