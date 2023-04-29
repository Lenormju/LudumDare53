import pygame

from GameInfo import GAME_INFO
from objects.Stork import Stork
from objects.Character import Character
from objects.Sounds import background_sound, explosion_sound
from objects.Animation import Animation
import random

background_sound.play(loops=-1)

comic_sans_ms = pygame.font.SysFont('Comic Sans MS', 30)

alien_image1 = pygame.image.load("assets/alien.png")
enemies = []
enemies.append(Stork(alien_image1, 0, 0))
enemies.append(Stork(alien_image1, 120, 0))
enemies.append(Stork(alien_image1, 300, 0))

character = Character(pygame.Rect(GAME_INFO.SCREEN_WIDTH/2, GAME_INFO.SCREEN_HEIGHT-100, 100, 100), 10, "assets/kaizen.png")
player_has_lost = False

animations = []


def render(screen, events, keys):
    global enemies, player_has_lost

    def DetermineEndGame():
        if player_has_lost:
            character.rect = pygame.Rect(5000, 5000, 0, 0)  # out of sight !
            ColoredTextEnd((255, 0, 0), 'You have lost!')
        else:
            if not enemies:
                ColoredTextEnd((0, 255, 0), 'You have win!')
            screen.blit(character.image, character.rect)

    def ColoredTextEnd(color, text):
        text_surface = comic_sans_ms.render(text, False, color)
        screen.blit(text_surface, (0, 0))

    def AnimationsShoots():
        for key, val in character.ApplyShoots(screen, enemies).items():
            animations.append(Animation(lambda: screen.blit(key.image, key.rect)))
            enemies.remove(val)

        for animation in animations:
            isPlay = animation.Increment()
            if not isPlay:
                animations.remove(animation)
    
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

    black_color = (0, 0, 0)
    screen.fill(black_color)  # === draw _AFTER_ this line ===

    for enemy in enemies:
        enemy.Move(screen)
    if shooting:
        character.DoShoot(screen)

    DropAndMoveBabies()
    AnimationsShoots()

    # check if alien destroys the player
    for enemy in enemies:
        if enemy.rect.colliderect(character.rect):
            explosion_sound.play()
            player_has_lost = True
            break

    DetermineEndGame()
