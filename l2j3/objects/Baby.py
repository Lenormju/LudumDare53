from objects.Thing import Thing
from GameInfo import GAME_INFO
import pygame
from random import *

class Baby(Thing):
    def SetType(self, type):
        self.type = type

    def GoToDown(self):
        if self.rect.y < GAME_INFO.SCREEN_HEIGHT + self.speedy:
            self.Move(self.speedx, self.speedy)
            return True
        if self.rect.y >= GAME_INFO.SCREEN_HEIGHT + self.speedy:
            return False
        
    def isCollideBabies(self, rect):        
        if(self.rect.colliderect(rect)):
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
