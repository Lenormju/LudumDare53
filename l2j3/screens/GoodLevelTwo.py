import pygame

from GameInfo import GAME_INFO, GameScreen
from objects.Stork import Stork
from objects.Unicorn import Unicorn
from objects.Direction import Direction
from objects.DropType import DropType
from objects.CharacterGoodLevel2 import CharacterGoodLevel2
from objects.Animation import Animation
from objects.Sounds import down_turn_sound, play_sound
from objects.Mouse import MouseButtons
from objects.Baby import Baby
from objects.Colors import *
from random import *

comic_sans_ms = pygame.font.SysFont('Comic Sans MS', 30)

imageInTheBox = pygame.image.load("assets/in_the_box.png").convert_alpha()
imageInTheBox = pygame.transform.scale(imageInTheBox, (100,100))
imageNotGoodBox = pygame.image.load("assets/not_good_box.png").convert_alpha()
imageNotGoodBox = pygame.transform.scale(imageNotGoodBox, (100,100))
enemies_images = []
enemies_images.append(pygame.image.load("assets/stork_blue_1.png"))
enemies_images.append(pygame.image.load("assets/stork_blue_2.png"))
unicorn_image = pygame.image.load("assets/unicorn.png")


def init_level():
    global enemies, unicorns, babies, poops, character, player_has_lost, firstTick, animations_youpi, start_ticks
    enemies = []
    unicorns = []
    babies = []
    poops = []
    number_of_enemies = 15
    for _ in range(number_of_enemies):
        enemies.append(Stork(enemies_images,
                            randint(0, GAME_INFO.SCREEN_WIDTH),
                            randint(0, GAME_INFO.SCREEN_HEIGHT/2)))
    unicorn_number = 5
    for _ in range(unicorn_number):
        direction = choice([Direction.LEFT, Direction.RIGHT])
        unicorns.append(Unicorn(unicorn_image,
                        direction,
                        0 if direction == Direction.RIGHT else GAME_INFO.SCREEN_WIDTH,
                        randint(0, GAME_INFO.SCREEN_HEIGHT/2),
                        randint(60, 1000)))

    character = CharacterGoodLevel2()
    player_has_lost = False
    firstTick = True

    animations_youpi = []
    start_ticks = 0

def render(screen, events, keys, mouse_buttons: MouseButtons):
    global enemies, unicorns, babies, poops, character, player_has_lost, firstTick, animations_youpi, start_ticks
    if firstTick:
        start_ticks=pygame.time.get_ticks()
        firstTick = False

    def ClearBoard(nextScreen):
        character = None
        enemies.clear()
        unicorns.clear()
        babies.clear()
        GAME_INFO.NEXT_GAME_SCREEN = nextScreen

    def DetermineEndGame():
        global character, enemies, unicorns
        if not enemies and not unicorns:
            if GAME_INFO.SCORE >= 15:
                ClearBoard(GameScreen.GOOD_LEVEL_TWO_INTERLUDE)
            else:
                ClearBoard(GameScreen.NEUTRAL_ENDING)
            
        else:
            pass  # on continue le jeu

    def ColoredTextEnd(color, text, x = 0, y = 0):
        text_surface = comic_sans_ms.render(text, False, color)
        screen.blit(text_surface, (x, y))

    
    def DropAndMoveBabies():
        if unicorns:
            unicorn = choice(unicorns)
            if not unicorn.waiting and GAME_INFO.CURRENT_TICK_NUMBER % randint(30, 60) == 0:
                DropBaby(unicorn)
        if enemies:
            enemy = choice(enemies)
            if GAME_INFO.CURRENT_TICK_NUMBER % randint(30, 90) == 0:
                DropBaby(enemy)
        for baby in babies:
            isMoving = baby.ApplyMoveBaby(screen)
            if not isMoving:
                babies.remove(baby)

    def DropBaby(enemy):
        baby = Baby(enemy.rect, 0, randint(1, 10), enemy.baby_picture_path)
        baby.SetType(enemy.type)
        babies.append(baby)
        screen.blit(baby.image, baby.rect)
        play_sound(down_turn_sound)
        return baby

    if (pygame.mouse.get_pos()[0] - character.panierBaby.rect.x) < 0:
        character.GoToLeft()
    elif (pygame.mouse.get_pos()[0] - character.panierBaby.rect.x) > 0:
        character.GoToRight()

    screen.fill(sky_color)  # === draw _AFTER_ this line ===

    screen.blit(character.panierBaby.image, character.panierBaby.rect)
    screen.blit(character.panierPoop.image, character.panierPoop.rect)
    
    for enemy in enemies + unicorns:
        enemy.Move(screen)
        if enemy.HasExit(screen) and enemy.type == DropType.BABY_TYPE:
            enemies.remove(enemy)
        if enemy.HasExit(screen) and enemy.type == DropType.POOP_TYPE:
            unicorns.remove(enemy)
    

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
                elif isCollideBabyInPoop:
                    #on fait +1 dans isCollideBabies donc -2+1 = -1
                    GAME_INFO.SCORE -= 2
                    animation.animation = lambda: screen.blit(imageNotGoodBox, pygame.Rect(character.panierPoop.rect.x, character.panierPoop.rect.y-100, 100,100))
            elif baby.type is DropType.POOP_TYPE:
                isCollidePoopInPoop = baby.isCollideBabies(character.panierPoop)
                isCollidePoopInBaby = baby.isCollideBabies(character.panierBaby)
                if isCollidePoopInPoop:
                    #on fait +1 dans isCollideBabies donc 1+2 = +3
                    GAME_INFO.SCORE += 2
                    animation.animation = lambda: screen.blit(imageInTheBox, pygame.Rect(character.panierPoop.rect.x, character.panierPoop.rect.y-100, 100,100))
                elif isCollidePoopInBaby:
                    #on fait +1 dans isCollideBabies donc -4+1 = -3
                    GAME_INFO.SCORE -= 4
                    animation.animation = lambda: screen.blit(imageNotGoodBox, pygame.Rect(character.panierBaby.rect.x, character.panierBaby.rect.y-100, 100,100))
            
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
