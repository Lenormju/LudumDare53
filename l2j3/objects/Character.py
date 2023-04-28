import pygame
from objects.Thing import Thing
from objects.Shoot import Shoot

class Character(Thing):
    shoots = []
    def GoToRight(self, xScreen):
        if self.rect.x + self.rect.width < xScreen + self.speed:
            self.Move(self.speed, 0)
    
    def GoToLeft(self):
        if self.rect.x >= self.speed:
            self.Move(-self.speed, 0)
    
    def DoShoot(self, screen):
        shoot = Shoot(pygame.Rect(self.rect.x, self.rect.y, 50, 50), 10, "assets/shoot.png")
        self.shoots.append(shoot)
        screen.blit(shoot.image, shoot.rect)

    def ApplyShoots(self, screen, ennemies):
        destroying = []
        for shoot in self.shoots:
            isMoving = shoot.GoToUp()
            isDestroy = shoot.isCollideEnnemy(ennemies)
            if isDestroy is not None:
                self.shoots.remove(shoot)
                destroying.append(isDestroy)
            
            if isMoving:
                screen.blit(shoot.image, shoot.rect)
            if not isMoving:
                self.shoots.remove(shoot)
            
        return destroying