from objects.Thing import Thing
from GameInfo import GAME_INFO
import pygame

class Baby(Thing):
    def GoToDown(self):
        if self.rect.y < GAME_INFO.SCREEN_HEIGHT + self.speed:
            self.Move(0, self.speed)
            return True
        if self.rect.y >= GAME_INFO.SCREEN_HEIGHT + self.speed:
            return False
        