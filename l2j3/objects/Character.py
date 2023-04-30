import pygame
from objects.Thing import Thing
from objects.Shoot import Shoot
from GameInfo import GAME_INFO

class Character(Thing):
    shoots = []

    def GoToRight(self):
        if self.rect.x + self.rect.width < GAME_INFO.SCREEN_WIDTH + self.speedx:
            distance_to_mouse_x = pygame.mouse.get_pos()[0] - self.rect.x
            speedx = min(self.speedx, distance_to_mouse_x)
            self.Move(speedx, self.speedy)

    def GoToLeft(self):
        if self.rect.x >= self.speedx:
            distance_to_mouse_x = self.rect.x - pygame.mouse.get_pos()[0]
            speedx = max(-self.speedx, -distance_to_mouse_x)
            self.Move(speedx, self.speedy)
    
    def DoShoot(self, screen):
        shoot = Shoot(pygame.Rect(self.rect.x+3, self.rect.y-15, 15, 20), 0, 10, "assets/shoot.png")
        self.shoots.append(shoot)
        screen.blit(shoot.image, shoot.rect)
    
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