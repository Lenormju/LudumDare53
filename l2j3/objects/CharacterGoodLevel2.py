import pygame
from objects.Panier import PanierGun
from GameInfo import GAME_INFO
from objects.DropType import DropType

class CharacterGoodLevel2():
    def __init__(self):
        self.panierBaby = PanierGun(pygame.Rect(GAME_INFO.SCREEN_WIDTH/2, GAME_INFO.SCREEN_HEIGHT-75,100, 75), 15, 0, "assets/panier_baby.png")
        self.panierBaby.SetType(DropType.BABY_TYPE)
        self.panierPoop = PanierGun(pygame.Rect(GAME_INFO.SCREEN_WIDTH/2-110, GAME_INFO.SCREEN_HEIGHT-75,100, 75), 15, 0, "assets/panier_poop.png")
        self.panierPoop.SetType(DropType.POOP_TYPE)

    def GoToRight(self):
        if self.panierPoop.rect.x + self.panierPoop.rect.width < GAME_INFO.SCREEN_WIDTH + self.panierPoop.speedx:
            distance_to_mouse_x = pygame.mouse.get_pos()[0] - self.panierBaby.rect.x
            speedx = min(self.panierPoop.speedx, distance_to_mouse_x)
            self.panierBaby.rect = self.panierBaby.rect.move(speedx, self.panierBaby.speedy)
            self.panierPoop.rect = self.panierPoop.rect.move(speedx, self.panierPoop.speedy)

    def GoToLeft(self):
        if self.panierBaby.rect.x >= self.panierBaby.speedx:
            distance_to_mouse_x = self.panierBaby.rect.x - pygame.mouse.get_pos()[0]
            speedx = max(-self.panierBaby.speedx, -distance_to_mouse_x)
            self.panierBaby.rect = self.panierBaby.rect.move(speedx, self.panierBaby.speedy)
            self.panierPoop.rect = self.panierPoop.rect.move(speedx, self.panierPoop.speedy)
