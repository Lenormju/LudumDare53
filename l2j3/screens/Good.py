import pygame

from GameInfo import GAME_INFO, GameScreen
from objects.Stork import Stork
from objects.Character import Character
from objects.Sounds import background_sound, explosion_sound
from objects.Animation import Animation
from objects.Shoot import Shoot
from objects.Colors import *
import random

background_sound.play(loops=-1)

comic_sans_ms = pygame.font.SysFont('Comic Sans MS', 30)

enemies_images = []
enemies_images.append(pygame.image.load("assets/stork_blue_1.png"))
enemies_images.append(pygame.image.load("assets/stork_blue_2.png"))
enemies = []
enemies.append(Stork(enemies_images, 0, 0))
enemies.append(Stork(enemies_images, 120, 0))
enemies.append(Stork(enemies_images, 300, 0))
enemies.append(Stork(enemies_images, 172, 80))
enemies.append(Stork(enemies_images, 290, 150))
enemies.append(Stork(enemies_images, 160, 198))

character = Character(pygame.Rect(GAME_INFO.SCREEN_WIDTH/2, GAME_INFO.SCREEN_HEIGHT-100, 100, 100), 10, "assets/kaizen.png")
player_has_lost = False

shoot_animations = []

def render(screen, events, keys):
    global enemies, player_has_lost

    def DetermineEndGame():
        if player_has_lost:
            character.rect = pygame.Rect(5000, 5000, 0, 0)  # out of sight !
            ColoredTextEnd((255, 0, 0), 'You have lost!')
        else:
            if not enemies:
                ColoredTextEnd((0, 255, 0), 'You have win!')
                # TODO: remove character and enemies' sounds !
                GAME_INFO.NEXT_GAME_SCREEN = GameScreen.GAME_GOOD_ENDING_GOOD
            screen.blit(character.image, character.rect)

    def ColoredTextEnd(color, text, x = 0, y = 0):
        text_surface = comic_sans_ms.render(text, False, color)
        screen.blit(text_surface, (x, y))

    def AnimationsShoots():
        for shoot, enemy in character.ApplyShoots(screen, enemies).items():
            animation = Animation(10)
            def my_anim_action():
                nonlocal shoot
                if animation.currentTick <= (animation.duration // 2):
                    screen.blit(shoot.image, shoot.rect)
                else:
                    shoot.UpdateImage("assets/shoot_explosion_max.png", 100, 50)
                    screen.blit(shoot.image, shoot.rect)
            animation.animation = my_anim_action
            shoot_animations.append(animation)
            enemies.remove(enemy)

        for animation in shoot_animations:
            isPlay = animation.Increment()
            if not isPlay:
                shoot_animations.remove(animation)

    def DropAndMoveBabies():
        if GAME_INFO.CURRENT_TICK_NUMBER % 60 == 0:
            if enemies:
                stork = random.choice(enemies)
                stork.DropBaby(screen)
        for enemy in enemies:
            for baby in enemy.babies:
                enemy.ApplyMoveBaby(baby, screen)

    shooting = False

    if keys[pygame.K_LEFT]:
        character.GoToLeft()
    if keys[pygame.K_RIGHT]:
        character.GoToRight()

    for event in events:
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            shooting = True

    screen.fill(sky_color)  # === draw _AFTER_ this line ===

    for enemy in enemies:
        enemy.Move(screen)
    if shooting:
        character.DoShoot(screen)

    DropAndMoveBabies()
    AnimationsShoots()

    for enemy in enemies:
        enemy.isCollideBabies(character)
    ColoredTextEnd((0,0,0), "Score : "+str(GAME_INFO.SCORE), GAME_INFO.SCREEN_WIDTH-150, 0)
    ColoredTextEnd((0,0,0), "Timer : "+str(round(GAME_INFO.CURRENT_TICK_NUMBER / 60)), GAME_INFO.SCREEN_WIDTH/3, 0)

    # check if alien destroys the player
    for enemy in enemies:
        if enemy.rect.colliderect(character.rect):
            explosion_sound.play()
            player_has_lost = True
            break

    DetermineEndGame()
