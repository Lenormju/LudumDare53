import pygame
from objects.Thing import Thing
from objects.Panier import PanierGun
from objects.DropType import DropType
from objects.Shoot import Shoot
from GameInfo import GAME_INFO

class CharacterBadLevel2():
    shoots = []

    def __init__(self):
        self.gunLeft = PanierGun(pygame.Rect(GAME_INFO.SCREEN_WIDTH/2-110, GAME_INFO.SCREEN_HEIGHT-100,100, 100), 10, 0, "assets/gun_left.png")
        self.gunLeft.SetType(DropType.BABY_TYPE)
        self.gunRight = PanierGun(pygame.Rect(GAME_INFO.SCREEN_WIDTH/2, GAME_INFO.SCREEN_HEIGHT-100,100, 100), 10, 0, "assets/gun_right.png")
        self.gunRight.SetType(DropType.BABY_TYPE)

    def GoToRight(self):
        if self.gunLeft.rect.x + self.gunLeft.rect.width < GAME_INFO.SCREEN_WIDTH + self.gunLeft.speedx:
            self.gunLeft.rect = self.gunLeft.rect.move(self.gunLeft.speedx, self.gunLeft.speedy)
            self.gunRight.rect = self.gunRight.rect.move(self.gunRight.speedx, self.gunRight.speedy)
    
    def GoToLeft(self):
        if self.gunRight.rect.x >= self.gunRight.speedx:
            self.gunRight.rect = self.gunRight.rect.move(-self.gunRight.speedx, self.gunRight.speedy)
            self.gunLeft.rect = self.gunLeft.rect.move(-self.gunLeft.speedx, self.gunLeft.speedy)
    
    def DoShoot(self, screen):
        shoot1 = Shoot(pygame.Rect(self.gunLeft.rect.x, self.gunLeft.rect.y, 50, 50), 0, 10, "assets/shoot.png")
        shoot2 = Shoot(pygame.Rect(self.gunRight.rect.x, self.gunRight.rect.y, 50, 50), 0, 10, "assets/shoot.png")
        self.shoots.append(shoot1)
        self.shoots.append(shoot2)
        screen.blit(shoot1.image, shoot1.rect)
        screen.blit(shoot2.image, shoot2.rect)
    
    def ApplyShoots(self, screen, ennemies):
        destroying = {}
        for shoot in self.shoots:
            isMoving = shoot.GoToUp()
            isDestroy = shoot.isCollideEnnemy(ennemies)
            if isDestroy is not None:
                self.shoots.remove(shoot)
                shoot.UpdateImage("assets/shoot_explosion_min.png", 50, 25)
                destroying[shoot] = isDestroy
            
            if isMoving:
                screen.blit(shoot.image, shoot.rect)
            if not isMoving:
                try:
                    self.shoots.remove(shoot)
                except ValueError:
                    pass
            
        return destroying