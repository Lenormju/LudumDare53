import pygame

from GameInfo import GAME_INFO, GameScreen
from objects.Stork import Stork
from objects.Character import Character
from objects.Sounds import explosion_sound, down_turn_sound, left_turn_sound, play_sound
from objects.Animation import Animation
from objects.Mouse import MouseButtons, MY_MOUSE_BUTTON_LEFT
from objects.Baby import Baby
from objects.Colors import *
from random import *

comic_sans_ms = pygame.font.SysFont('Comic Sans MS', 30)

enemies_images = []
enemies_images.append(pygame.image.load("assets/evil_stork1.png"))
enemies_images.append(pygame.image.load("assets/evil_stork2.png"))
bombexplosionimage = pygame.image.load("assets/explosion_bomb.png").convert_alpha()
bombexplosionimage = pygame.transform.scale(bombexplosionimage, (100,100))

def init_level():
    global enemies, babies, character, player_has_lost, firstTick, shoot_animations, bomb_animations, start_ticks
    enemies = []
    babies = []
    number_of_enemies = 30
    for _ in range(number_of_enemies):
        enemies.append(Stork(enemies_images,
                            randint(0, GAME_INFO.SCREEN_WIDTH),
                            randint(0, GAME_INFO.SCREEN_HEIGHT/2)))

    character = Character(pygame.Rect(GAME_INFO.SCREEN_WIDTH/2, GAME_INFO.SCREEN_HEIGHT-100, 75, 75), 15, 0, "assets/gun_left.png")
    player_has_lost = False
    firstTick = True

    shoot_animations = []
    bomb_animations = []
    start_ticks = 0
    

def render(screen, events, keys, mouse_buttons: MouseButtons):
    global enemies, babies, character, player_has_lost, firstTick, shoot_animations, bomb_animations, start_ticks
    if firstTick:
        start_ticks=pygame.time.get_ticks()
        firstTick = False

    def ClearBoard(nextScreen):
        character = None
        enemies.clear()
        babies.clear()
        GAME_INFO.NEXT_GAME_SCREEN = nextScreen

    def DetermineEndGame():
        global character, enemies
        if not enemies:
            if GAME_INFO.SCORE >= 15:
                ClearBoard(GameScreen.BAD_LEVEL_ONE_INTERLUDE)
            else:
                ClearBoard(GameScreen.NEUTRAL_ENDING)
            
        else:
            pass  # on continue le jeu

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
            animation.animation = my_anim_action
            shoot_animations.append(animation)
            try:
                enemies.remove(enemy)
            except ValueError:
                pass  # Lou dit que c'est sans danger, on verra bien .....

        for animation in shoot_animations:
            isPlay = animation.Increment()
            if not isPlay:
                shoot_animations.remove(animation)

    def DropAndMoveBabies():
        if GAME_INFO.CURRENT_TICK_NUMBER % randint(30, 90) == 0:
            if enemies:
                stork = choice(enemies)
                DropBaby(stork)
        for baby in babies:
            isMoving = baby.ApplyMoveBaby(screen)
            if not isMoving:
                babies.remove(baby)
                GAME_INFO.SCORE += 1  # contrebalancer le fait qu'on l'ait enlevé auparavant

    def DropBaby(stork):
        baby = Baby(stork.rect.scale_by(0.5), 0, randint(1, 10), "assets/bomb.png")
        babies.append(baby)
        screen.blit(baby.image, baby.rect)
        play_sound(down_turn_sound)
        return baby

    shooting = False

    if (pygame.mouse.get_pos()[0] - character.rect.x) < 0:
        character.GoToLeft()
    elif (pygame.mouse.get_pos()[0] - character.rect.x) > 0:
        character.GoToRight()

    for event in events:
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == MY_MOUSE_BUTTON_LEFT:
            shooting = True

    screen.fill(evil_red)  # === draw _AFTER_ this line ===

    screen.blit(character.image, character.rect)
    for enemy in enemies:
        enemy.Move(screen)
        if enemy.HasExit(screen):
            enemies.remove(enemy)
    
    if shooting:
        character.DoShoot(screen)

    DropAndMoveBabies()
    AnimationsShoots()

    for baby in babies:
        isCollide = baby.isCollideBabies(character)
        if isCollide:
            animation = Animation(15)
            animation.animation = lambda: screen.blit(bombexplosionimage, pygame.Rect(character.rect.x-20, character.rect.y, 100,100))
            play_sound(left_turn_sound)
            GAME_INFO.SCORE -= 4
            babies.remove(baby)
            bomb_animations.append(animation)
        
    for anim in bomb_animations:
        isRunning = anim.Increment()
        if not isRunning:
            bomb_animations.remove(anim)
    seconds=(pygame.time.get_ticks()-start_ticks)/1000
    ColoredTextEnd((0,0,0), "Score : "+str(GAME_INFO.SCORE), GAME_INFO.SCREEN_WIDTH-150, 0)
    ColoredTextEnd((0,0,0), "Timer : "+str(round(seconds)), GAME_INFO.SCREEN_WIDTH/3, 0)

    # check if alien destroys the player
    for enemy in enemies:
        if enemy.rect.colliderect(character.rect):
            play_sound(explosion_sound)
            player_has_lost = True
            break

    DetermineEndGame()
