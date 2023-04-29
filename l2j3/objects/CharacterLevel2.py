import pygame
from objects.Panier import Panier
from GameInfo import GAME_INFO
from objects.DropType import DropType

class CharacterLevel2():
    shoots = []
    def __init__(self):
        self.panierBaby = Panier(pygame.Rect(GAME_INFO.SCREEN_WIDTH/2, GAME_INFO.SCREEN_HEIGHT-100,100, 100), 10, 0, "assets/panier_baby.png")
        self.panierBaby.SetType(DropType.BABY_TYPE)
        self.panierPoop = Panier(pygame.Rect(GAME_INFO.SCREEN_WIDTH/2-110, GAME_INFO.SCREEN_HEIGHT-100,100, 100), 10, 0, "assets/panier_poop.png")
        self.panierPoop.SetType(DropType.POOP_TYPE)

    def GoToRight(self):
        if self.panierPoop.rect.x + self.panierPoop.rect.width < GAME_INFO.SCREEN_WIDTH + self.panierPoop.speedx:
            self.panierBaby.rect = self.panierBaby.rect.move(self.panierBaby.speedx, self.panierBaby.speedy)
            self.panierPoop.rect = self.panierPoop.rect.move(self.panierPoop.speedx, self.panierPoop.speedy)
    
    def GoToLeft(self):
        if self.panierBaby.rect.x >= self.panierBaby.speedx:
            self.panierBaby.rect = self.panierBaby.rect.move(-self.panierBaby.speedx, self.panierBaby.speedy)
            self.panierPoop.rect = self.panierPoop.rect.move(-self.panierPoop.speedx, self.panierPoop.speedy)