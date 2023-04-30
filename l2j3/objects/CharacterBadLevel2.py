import pygame
from objects.Sounds import *
from objects.Panier import PanierGun
from objects.DropType import DropType
from objects.Shoot import Shoot
from GameInfo import GAME_INFO

class CharacterBadLevel2():
    shoots = []

    def __init__(self):
        self.gunLeft = PanierGun(pygame.Rect(GAME_INFO.SCREEN_WIDTH/2-50, GAME_INFO.SCREEN_HEIGHT-100,75, 75), 15, 0, "assets/gun_left.png")
        self.gunLeft.SetType(DropType.BABY_TYPE)
        self.gunRight = PanierGun(pygame.Rect(GAME_INFO.SCREEN_WIDTH/2, GAME_INFO.SCREEN_HEIGHT-100,75, 75), 15, 0, "assets/gun_right.png")
        self.gunRight.SetType(DropType.BABY_TYPE)

    def GoToRight(self):
        if self.gunLeft.rect.x + self.gunLeft.rect.width < GAME_INFO.SCREEN_WIDTH + self.gunLeft.speedx:
            distance_to_mouse_x = pygame.mouse.get_pos()[0] - self.gunRight.rect.x
            speedx = min(self.gunLeft.speedx, distance_to_mouse_x)
            self.gunRight.rect = self.gunRight.rect.move(speedx, self.gunRight.speedy)
            self.gunLeft.rect = self.gunLeft.rect.move(speedx, self.gunLeft.speedy)

    def GoToLeft(self):
        if self.gunRight.rect.x >= self.gunRight.speedx:
            distance_to_mouse_x = self.gunRight.rect.x - pygame.mouse.get_pos()[0]
            speedx = max(-self.gunRight.speedx, -distance_to_mouse_x)
            self.gunRight.rect = self.gunRight.rect.move(speedx, self.gunRight.speedy)
            self.gunLeft.rect = self.gunLeft.rect.move(speedx, self.gunLeft.speedy)

    def DoShootLeft(self, screen):
        shoot = Shoot(pygame.Rect(self.gunLeft.rect.x+2, self.gunLeft.rect.y-15, 15, 20), 0, 10, "assets/shoot.png")
        self.shoots.append(shoot)
        screen.blit(shoot.image, shoot.rect)
        play_sound(shoot_sound)

    def DoShootRight(self, screen):
        shoot = Shoot(pygame.Rect(self.gunRight.rect.x+56, self.gunRight.rect.y-15, 15, 20), 0, 10, "assets/shoot.png")
        self.shoots.append(shoot)
        screen.blit(shoot.image, shoot.rect)
        play_sound(shoot_sound)
    
    def ApplyShoots(self, screen, ennemies):
        destroying = {}
        for shoot in self.shoots:
            isMoving = shoot.GoToUp()
            isDestroy = shoot.isCollideEnnemy(ennemies)
            if isDestroy is not None:
                self.shoots.remove(shoot)
                shoot.UpdateImage("assets/shoot_explosion_min.png", 30, 30)
                destroying[shoot] = isDestroy
            
            if isMoving:
                screen.blit(shoot.image, shoot.rect)
            if not isMoving:
                try:
                    self.shoots.remove(shoot)
                except ValueError:
                    pass
            
        return destroying