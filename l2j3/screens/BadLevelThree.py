import pygame

from GameInfo import GAME_INFO, GameScreen
from objects.Mouse import MouseButtons, MY_MOUSE_BUTTON_LEFT, MY_MOUSE_BUTTON_RIGHT
from objects.DropType import DropType
from objects.BigUnicorn import BigUnicorn
from objects.Character import Character
from objects.Sounds import *
from objects.Animation import Animation
from objects.Baby import Baby
from objects.Colors import *
from random import *

comic_sans_ms = pygame.font.SysFont('Comic Sans MS', 30)

boss_enemies = []
boss_enemies.append(pygame.image.load("assets/stork_boss_form1_1.png"))
boss_enemies.append(pygame.image.load("assets/stork_boss_form1_2.png"))
enemies_images = []
enemies_images.append(pygame.image.load("assets/stork_boss_form1_1.png"))
enemies_images.append(pygame.image.load("assets/stork_boss_form1_2.png"))

backgroundbad = pygame.image.load("assets/backgroundevil.png")
backgroundbad = pygame.transform.scale(backgroundbad, (GAME_INFO.SCREEN_WIDTH,GAME_INFO.SCREEN_HEIGHT))
backgroundbad = backgroundbad.convert()

def init_level():
    global enemies, babies, character, player_has_lost, firstTick, shoot_animations, start_ticks, has_started_music
    enemies = []
    babies = []
    number_of_enemies = 1
    for _ in range(number_of_enemies):
        enemies.append(BigUnicorn(enemies_images,
                                20,
                                0,
                                200))

    character = Character(pygame.Rect(GAME_INFO.SCREEN_WIDTH/2, GAME_INFO.SCREEN_HEIGHT-100, 75, 75), 10, 0, "assets/gun_left.png")
    player_has_lost = False
    firstTick = True

    shoot_animations = []
    start_ticks = 0
    has_started_music = False

def render(screen, events, keys, mouse_buttons: MouseButtons):
    global enemies, babies, character, player_has_lost, firstTick, shoot_animations, start_ticks, has_started_music
    if firstTick:
        start_ticks=pygame.time.get_ticks()
        firstTick = False

    if not has_started_music:
        has_started_music = True
        play_music(boss_stork_sound)
        play_music_next(metal_bad2_music)

    def ClearBoard(nextScreen):
        character = None
        enemies.clear()
        babies.clear()
        GAME_INFO.NEXT_GAME_SCREEN = nextScreen

    def DetermineEndGame():
        global character, enemies
        if not enemies:
            if GAME_INFO.SCORE > 15:
                ClearBoard(GameScreen.BAD_ENDING)
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
                else:
                    shoot.UpdateImage("assets/shoot_explosion_max.png", 30, 30)
                    screen.blit(shoot.image, shoot.rect)
            animation.animation = my_anim_action
            shoot_animations.append(animation)
            enemies.remove(enemy)

        for animation in shoot_animations:
            isPlay = animation.Increment()
            if not isPlay:
                shoot_animations.remove(animation)

    def DropAndMoveBabies():
        if enemies:
            stork = choice(enemies)
            if stork.type == DropType.POOP_TYPE and GAME_INFO.CURRENT_TICK_NUMBER % randint(15, 30) == 0:
                DropBaby(stork.rect.scale_by(0.5))
            if stork.type == DropType.BABY_TYPE and GAME_INFO.CURRENT_TICK_NUMBER % randint(30, 90) == 0:
                DropBaby(stork.rect)
        for baby in babies:
            isMoving = baby.ApplyMoveBaby(screen)
            if not isMoving:
                babies.remove(baby)
                GAME_INFO.SCORE += 1  # contrebalancer le fait qu'on l'ait enlevé auparavant

    def DropBaby(rect):
        baby = Baby(rect.scale_by(0.5),  randint(-3, 3), randint(1, 10), "assets/bomb.png")
        babies.append(baby)
        screen.blit(baby.image, rect)
        # TODO: sound ?
        return baby

    shooting = False

    if (pygame.mouse.get_pos()[0] - character.rect.x) < 0:
        character.GoToLeft()
    elif (pygame.mouse.get_pos()[0] - character.rect.x) > 0:
        character.GoToRight()

    for event in events:
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == MY_MOUSE_BUTTON_LEFT:
            shooting = True
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == MY_MOUSE_BUTTON_RIGHT:
            shooting = True


    # screen.fill(evil_red)  # === draw _AFTER_ this line ===
    screen.blit(backgroundbad, pygame.Rect((0,0),(GAME_INFO.SCREEN_WIDTH,GAME_INFO.SCREEN_HEIGHT)))  # === draw _AFTER_ this line ===

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
            babies.remove(baby)
        
    seconds=(pygame.time.get_ticks()-start_ticks)/1000
    ColoredTextEnd((255,0,0), "Score : "+str(GAME_INFO.SCORE), GAME_INFO.SCREEN_WIDTH-150, 0)
    ColoredTextEnd((255,0,0), "Timer : "+str(round(seconds)), GAME_INFO.SCREEN_WIDTH/3, 0)

    # check if alien destroys the player
    for enemy in enemies:
        if enemy.rect.colliderect(character.rect):
            play_sound(explosion_sound)
            player_has_lost = True
            break

    DetermineEndGame()
