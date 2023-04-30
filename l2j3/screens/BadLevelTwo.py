import pygame

from GameInfo import GAME_INFO, GameScreen
from objects.Stork import Stork
from objects.CharacterBadLevel2 import CharacterBadLevel2
from objects.Sounds import *
from objects.Animation import Animation
from objects.Mouse import MouseButtons, MY_MOUSE_BUTTON_LEFT, MY_MOUSE_BUTTON_RIGHT
from objects.Baby import Baby
from objects.Colors import *
from random import *

comic_sans_ms = pygame.font.SysFont('Comic Sans MS', 30)

enemies_images = []
enemies_images.append(pygame.image.load("assets/evil_stork1.png"))
enemies_images.append(pygame.image.load("assets/evil_stork2.png"))

backgroundbad = pygame.image.load("assets/backgroundevil.png")
backgroundbad = pygame.transform.scale(backgroundbad, (GAME_INFO.SCREEN_WIDTH,GAME_INFO.SCREEN_HEIGHT))
backgroundbad = backgroundbad.convert()

bombexplosionimage = pygame.image.load("assets/explosion_bomb.png").convert_alpha()
bombexplosionimage = pygame.transform.scale(bombexplosionimage, (100,100))

def init_level():
    global enemies, babies, character, player_has_lost, firstTick, shoot_animations, bomb_animations, start_ticks, has_started_music
    enemies = []
    babies = []
    number_of_enemies = 200
    for _ in range(number_of_enemies):
        enemies.append(Stork(enemies_images,
                            randint(-2000, 2000 + GAME_INFO.SCREEN_WIDTH),
                            randint(0, GAME_INFO.SCREEN_HEIGHT/4)))

    character = CharacterBadLevel2()
    player_has_lost = False
    firstTick = True

    shoot_animations = []
    bomb_animations = []
    start_ticks = 0
    

    has_started_music = False

def render(screen, events, keys, mouse_buttons: MouseButtons):
    global enemies, babies, character, player_has_lost, firstTick, shoot_animations, bomb_animations, start_ticks, has_started_music
    if firstTick:
        start_ticks=pygame.time.get_ticks()
        firstTick = False

    if not has_started_music:
        has_started_music = True
        play_music(metal_bad2_music)

    def ClearBoard(nextScreen):
        character = None
        enemies.clear()
        babies.clear()
        GAME_INFO.NEXT_GAME_SCREEN = nextScreen

    def DetermineEndGame():
        global character, enemies
        if not enemies:
            if GAME_INFO.SCORE >= 100:
                ClearBoard(GameScreen.BAD_LEVEL_TWO_INTERLUDE)
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
        if GAME_INFO.CURRENT_TICK_NUMBER % randint(10, 60) == 0:
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
        # TODO: sound ?
        return baby

    shootingLeft = False
    shootingRight = False

    if (pygame.mouse.get_pos()[0] - character.gunRight.rect.x) < 0:
        character.GoToLeft()
    elif (pygame.mouse.get_pos()[0] - character.gunRight.rect.x) > 0:
        character.GoToRight()

    for event in events:
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == MY_MOUSE_BUTTON_LEFT:
            shootingLeft = True
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == MY_MOUSE_BUTTON_RIGHT:
            shootingRight = True

    # screen.fill(evil_red)  # === draw _AFTER_ this line ===
    screen.blit(backgroundbad, pygame.Rect((0,0),(GAME_INFO.SCREEN_WIDTH,GAME_INFO.SCREEN_HEIGHT)))  # === draw _AFTER_ this line ===

    screen.blit(character.gunLeft.image, character.gunLeft.rect)
    screen.blit(character.gunRight.image, character.gunRight.rect)
    for enemy in enemies:
        enemy.Move(screen)
        if enemy.HasExit(screen):
            enemies.remove(enemy)

    if shootingLeft:
        character.DoShootLeft(screen)
    if shootingRight:
        character.DoShootRight(screen)

    DropAndMoveBabies()
    AnimationsShoots()

    for baby in babies:
        isCollideRight = baby.isCollideBabies(character.gunRight.rect)
        isCollideLeft = baby.isCollideBabies(character.gunLeft.rect)
        if isCollideRight or isCollideLeft:
            animation = Animation(15)
            GAME_INFO.SCORE -= 4
            babies.remove(baby)
            if isCollideRight:
                animation.animation = lambda: screen.blit(bombexplosionimage, pygame.Rect(character.gunRight.rect.x, character.gunRight.rect.y, 100,100))
                play_sound(bomb_sound)
            if isCollideLeft:
                animation.animation = lambda: screen.blit(bombexplosionimage, pygame.Rect(character.gunLeft.rect.x, character.gunLeft.rect.y, 100,100))
                play_sound(bomb_sound)
            
            bomb_animations.append(animation)
        
    for anim in bomb_animations:
        isRunning = anim.Increment()
        if not isRunning:
            bomb_animations.remove(anim)
    seconds=(pygame.time.get_ticks()-start_ticks)/1000
    ColoredTextEnd((0,0,0), "Score : "+str(GAME_INFO.SCORE), GAME_INFO.SCREEN_WIDTH-150, 0)
    ColoredTextEnd((0,0,0), "Timer : "+str(round(seconds)), GAME_INFO.SCREEN_WIDTH/3, 0)

    DetermineEndGame()
