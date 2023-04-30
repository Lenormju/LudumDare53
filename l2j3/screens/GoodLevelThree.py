import random

import pygame

from GameInfo import GAME_INFO, GameScreen
from objects.StorkGood3 import StorkGood3
from objects.Mouse import MouseButtons
from objects.BigUnicorn import BigUnicorn
from objects.DropType import DropType
from objects.CharacterGoodLevel2 import CharacterGoodLevel2
from objects.Sounds import *
from objects.Animation import Animation
from objects.Baby import Baby
from objects.Colors import *
from random import *

comic_sans_ms = pygame.font.SysFont('Comic Sans MS', 30)

storks_images = []
storks_images.append(pygame.image.load("assets/stork_blue_1.png"))
storks_images.append(pygame.image.load("assets/stork_blue_2.png"))
imageInTheBox = pygame.image.load("assets/in_the_box.png").convert_alpha()
imageInTheBox = pygame.transform.scale(imageInTheBox, (100,100))
imageNotGoodBox = pygame.image.load("assets/not_good_box.png").convert_alpha()
imageNotGoodBox = pygame.transform.scale(imageNotGoodBox, (100,100))
unicorn_images = [pygame.image.load("assets/unicorn_boss_1.png"),
                    pygame.image.load("assets/unicorn_boss_2.png"),
                    pygame.image.load("assets/unicorn_boss_3.png")]
def init_level():
    global enemies,babies,character,player_has_lost,firstTick,animations_youpi,start_ticks, has_started_music
    enemies = []
    babies = []
    number_of_storks = 6
    for _ in range(number_of_storks):
        enemies.append(StorkGood3(storks_images,
                                randint(50, GAME_INFO.SCREEN_WIDTH-50),
                                randint(0, 70)))
    
    enemies.append(BigUnicorn(unicorn_images, 120, 0, 150))
    character = CharacterGoodLevel2()
    player_has_lost = False
    firstTick = True
    animations_youpi = []
    start_ticks = 0
    has_started_music = False
    

def render(screen, events, keys, mouse_buttons: MouseButtons):
    global enemies,babies,character,player_has_lost,firstTick,animations_youpi,start_ticks, has_started_music
    if firstTick:
        start_ticks=pygame.time.get_ticks()
        firstTick = False

    if not has_started_music:
        has_started_music = True
        play_music_loop(nyan_music)

    def ClearBoard(nextScreen):
        character = None
        enemies.clear()
        babies.clear()
        GAME_INFO.NEXT_GAME_SCREEN = nextScreen

    def DetermineEndGame():
        global character, enemies
        if seconds >= 60:
            if GAME_INFO.SCORE >= 50:
                ClearBoard(GameScreen.GOOD_ENDING)
            else:
                ClearBoard(GameScreen.NEUTRAL_ENDING)
        else:
            pass  # on continue le jeu

    def ColoredTextEnd(color, text, x = 0, y = 0):
        text_surface = comic_sans_ms.render(text, False, color)
        screen.blit(text_surface, (x, y))

    
    def DropAndMoveBabies():
        if enemies:
            enemy = choice(enemies)
            if enemy.type == DropType.POOP_TYPE and GAME_INFO.CURRENT_TICK_NUMBER % randint(15, 30) == 0:
                if not enemy.waiting:
                    DropBaby(enemy, enemy.rect.scale_by(0.3))
                    play_sound(prout_sound)
            elif enemy.type == DropType.BABY_TYPE and GAME_INFO.CURRENT_TICK_NUMBER % randint(30, 90) == 0:
                DropBaby(enemy, enemy.rect)
                play_sound(baby_sound)
        for baby in babies:
            isMoving = baby.ApplyMoveBaby(screen)
            if not isMoving:
                babies.remove(baby)
                play_sound(miss_box_sound)

    def DropBaby(enemy, baby_rect):
        baby = Baby(baby_rect, randint(-3, 3) if enemy.type == DropType.POOP_TYPE else 0, randint(1, 10), enemy.baby_picture_path)
        baby.SetType(enemy.type)
        babies.append(baby)
        screen.blit(baby.image, baby_rect)
        return baby

    shooting = False

    if (pygame.mouse.get_pos()[0] - character.panierBaby.rect.x) < 0:
        character.GoToLeft()
    elif (pygame.mouse.get_pos()[0] - character.panierBaby.rect.x) > 0:
        character.GoToRight()

    screen.fill(sky_color)  # === draw _AFTER_ this line ===

    screen.blit(character.panierBaby.image, character.panierBaby.rect)
    screen.blit(character.panierPoop.image, character.panierPoop.rect)
    for enemy in enemies:
        enemy.Move(screen)
        if enemy.HasExit(screen):
            enemies.remove(enemy)
    
    if shooting:
        character.DoShoot(screen)

    DropAndMoveBabies()

    for baby in babies:
            animation = Animation(15)
            isCollideBabyInBaby = False
            isCollideBabyInPoop = False
            isCollidePoopInPoop = False
            isCollidePoopInBaby = False
            if baby.type is DropType.BABY_TYPE:
                isCollideBabyInBaby = baby.isCollideBabies(character.panierBaby)
                isCollideBabyInPoop = baby.isCollideBabies(character.panierPoop)
                if isCollideBabyInBaby:    
                    #on fait +1 dans isCollideBabies
                    animation.animation = lambda: screen.blit(imageInTheBox, pygame.Rect(character.panierBaby.rect.x, character.panierBaby.rect.y-100, 100,100))
                    play_sound(good_box_sound)
                elif isCollideBabyInPoop:
                    #on fait +1 dans isCollideBabies donc -2+1 = -1
                    GAME_INFO.SCORE -= 2
                    animation.animation = lambda: screen.blit(imageNotGoodBox, pygame.Rect(character.panierPoop.rect.x, character.panierPoop.rect.y-100, 100,100))
                    play_sound(bad_box_sound)
            elif baby.type is DropType.POOP_TYPE:
                isCollidePoopInPoop = baby.isCollideBabies(character.panierPoop)
                isCollidePoopInBaby = baby.isCollideBabies(character.panierBaby)
                if isCollidePoopInPoop:
                    #on fait +1 dans isCollideBabies donc 1+2 = +3
                    GAME_INFO.SCORE += 2
                    animation.animation = lambda: screen.blit(imageInTheBox, pygame.Rect(character.panierPoop.rect.x, character.panierPoop.rect.y-100, 100,100))
                    play_sound(good_box_sound)
                elif isCollidePoopInBaby:
                    #on fait +1 dans isCollideBabies donc -4+1 = -3
                    GAME_INFO.SCORE -= 4
                    animation.animation = lambda: screen.blit(imageNotGoodBox, pygame.Rect(character.panierBaby.rect.x, character.panierBaby.rect.y-100, 100,100))
                    play_sound(bad_box_sound)

            if isCollideBabyInBaby or isCollidePoopInPoop or isCollidePoopInBaby or isCollideBabyInPoop:
                animations_youpi.append(animation)
                babies.remove(baby)
        
    for anim in animations_youpi:
        if not anim.Increment():
            animations_youpi.remove(anim)

    seconds=(pygame.time.get_ticks()-start_ticks)/1000
    ColoredTextEnd((0,0,0), "Score : "+str(GAME_INFO.SCORE), GAME_INFO.SCREEN_WIDTH-150, 0)
    ColoredTextEnd((0,0,0), "Timer : "+str(round(seconds)), GAME_INFO.SCREEN_WIDTH/3, 0)


    DetermineEndGame()
