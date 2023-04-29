from objects.Thing import Thing
from GameInfo import GAME_INFO
import pygame
from random import *

class Baby(Thing):
    def GoToDown(self):
        if self.rect.y < GAME_INFO.SCREEN_HEIGHT + self.speed:
            self.Move(0, self.speed)
            return True
        if self.rect.y >= GAME_INFO.SCREEN_HEIGHT + self.speed:
            return False
        
    def isCollideBabies(self, character):        
        if(self.rect.colliderect(character.rect)):
            GAME_INFO.SCORE += 1
            return True
        return False
    
    def ApplyMoveBaby(self, screen):
        isMoving = self.GoToDown()
        if isMoving:
            screen.blit(self.image, self.rect)
            return True
        if not isMoving:
            GAME_INFO.SCORE -= 1
            return False
