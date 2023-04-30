import pygame

from GameInfo import GAME_INFO, GameScreen
from objects.Mouse import MouseButtons, MY_MOUSE_BUTTON_LEFT, MY_MOUSE_BUTTON_RIGHT
from objects.DropType import DropType
from objects.BigUnicorn import BigUnicorn
from objects.Unicorn import Unicorn
from objects.Direction import Direction
from objects.Character import Character
from objects.Sounds import *
from objects.Animation import Animation
from objects.Baby import Baby
from objects.Colors import *
from random import *

comic_sans_ms = pygame.font.SysFont('Comic Sans MS', 30)

boss_enemies_form1 = []
boss_enemies_form1.append(pygame.image.load("assets/stork_boss_form1_1.png"))
boss_enemies_form1.append(pygame.image.load("assets/stork_boss_form1_2.png"))
boss_enemies_form2 = []
boss_enemies_form2.append(pygame.image.load("assets/stork_boss_form2_1.png"))
boss_enemies_form2.append(pygame.image.load("assets/stork_boss_form2_2.png"))
boss_enemies_form3= []
boss_enemies_form3.append(pygame.image.load("assets/stork_boss_form3_1.png"))
boss_enemies_form3.append(pygame.image.load("assets/stork_boss_form3_2.png"))
enemies_images = []
enemies_images.append(pygame.image.load("assets/stork_boss_form1_1.png"))
enemies_images.append(pygame.image.load("assets/stork_boss_form1_2.png"))

backgroundbad = pygame.image.load("assets/backgroundevil.png")
backgroundbad = pygame.transform.scale(backgroundbad, (GAME_INFO.SCREEN_WIDTH,GAME_INFO.SCREEN_HEIGHT))
backgroundbad = backgroundbad.convert()

bombexplosionimage = pygame.image.load("assets/explosion_bomb.png").convert_alpha()
bombexplosionimage = pygame.transform.scale(bombexplosionimage, (100,100))

def init_level():
    global enemies, babies, character, player_has_lost, firstTick, shoot_animations, start_ticks, has_started_music, boss_life, stork_boss, bomb_animations, win_tick
    babies = []
    number_of_enemies = 200
    enemies = []
    for _ in range(number_of_enemies):
        direction = choice([Direction.LEFT, Direction.RIGHT])
        enemies.append(Unicorn(enemies_images,
                        direction,
                        0 if direction == Direction.RIGHT else GAME_INFO.SCREEN_WIDTH,
                        randint(0, GAME_INFO.SCREEN_HEIGHT/2),
                        randint(60, 10000)))
    stork_boss = BigUnicorn(boss_enemies_form1,20,0, 200)
    stork_boss.type = DropType.BABY_TYPE
    enemies.append(stork_boss)
    character = Character(pygame.Rect(GAME_INFO.SCREEN_WIDTH/2, GAME_INFO.SCREEN_HEIGHT-100, 75, 75), 10, 0, "assets/gun_left.png")
    player_has_lost = False
    firstTick = True
    boss_life = 100

    bomb_animations = []
    shoot_animations = []
    start_ticks = 0
    has_started_music = False
    win_tick = 0

def render(screen, events, keys, mouse_buttons: MouseButtons):
    global enemies, babies, character, player_has_lost, firstTick, shoot_animations, start_ticks, has_started_music, boss_life, stork_boss, win_tick
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
        global character, boss_life, win_tick
        if boss_life <= 0:
            win_tick += 1
            if win_tick > 30:
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
        global boss_life
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
            if enemy.type == DropType.BABY_TYPE:
                boss_life -= 1
                if boss_life <= 0:
                    GAME_INFO.SCORE += 1
                    enemies.remove(enemy)
                elif boss_life <= 33:
                    enemy.SetImages(boss_enemies_form3)
                elif boss_life <= 75:
                    enemy.SetImages(boss_enemies_form2)
                GAME_INFO.SCORE -= 1
            else:
                enemies.remove(enemy)

        for animation in shoot_animations:
            isPlay = animation.Increment()
            if not isPlay:
                shoot_animations.remove(animation)

    def DropAndMoveBabies():
        global stork_boss
        if enemies:
            stork = choice(enemies)
            if GAME_INFO.CURRENT_TICK_NUMBER % randint(60, 150) == 0:
                DropBaby(stork_boss.rect.scale_by(0.5))
            if stork.type == DropType.POOP_TYPE and GAME_INFO.CURRENT_TICK_NUMBER % randint(30, 90) == 0:
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
            animation = Animation(15)
            animation.animation = lambda: screen.blit(bombexplosionimage, pygame.Rect(character.rect.x, character.rect.y, 100,100))
            play_sound(bomb_sound)
            GAME_INFO.SCORE -= 4
            babies.remove(baby)
            bomb_animations.append(animation)
        
    for anim in bomb_animations:
        isRunning = anim.Increment()
        if not isRunning:
            bomb_animations.remove(anim)
        
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
