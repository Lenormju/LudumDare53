import pygame

from GameInfo import GAME_INFO, GameScreen
from objects.Stork import Stork
from objects.Character import Character
from objects.Animation import Animation
from objects.Sounds import explosion_sound, down_turn_sound, play_sound
from objects.Mouse import MouseButtons
from objects.Baby import Baby
from objects.Colors import *
from random import *

comic_sans_ms = pygame.font.SysFont('Comic Sans MS', 30)

enemies_images = []
enemies_images.append(pygame.image.load("assets/stork_blue_1.png"))
enemies_images.append(pygame.image.load("assets/stork_blue_2.png"))
enemies = []
babies = []
number_of_enemies = 15
for _ in range(number_of_enemies):
    enemies.append(Stork(enemies_images,
                         randint(0, GAME_INFO.SCREEN_WIDTH),
                         randint(0, GAME_INFO.SCREEN_HEIGHT/2)))

character = Character(pygame.Rect(GAME_INFO.SCREEN_WIDTH/2, GAME_INFO.SCREEN_HEIGHT-100, 100, 100), 15, 0, "assets/panier.png")
player_has_lost = False
firstTick = True

imageInTheBox = pygame.image.load("assets/in_the_box.png").convert_alpha()
imageInTheBox = pygame.transform.scale(imageInTheBox, (100,100))
shoot_animations = []
start_ticks = 0

def render(screen, events, keys, mouse_buttons: MouseButtons):
    global enemies, player_has_lost, character, babies, firstTick,start_ticks
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
                ClearBoard(GameScreen.GOOD_LEVEL_TWO)
            elif GAME_INFO.SCORE < 0:
                ClearBoard(GameScreen.BAD_INTRO)
            else:
                ClearBoard(GameScreen.NEUTRAL_ENDING)
            GAME_INFO.SCORE = 0
        else:
            pass  # on continue le jeu

    def ColoredTextEnd(color, text, x = 0, y = 0):
        text_surface = comic_sans_ms.render(text, False, color)
        screen.blit(text_surface, (x, y))

    def DropAndMoveBabies():
        if GAME_INFO.CURRENT_TICK_NUMBER % randint(30, 90) == 0:
            if enemies:
                stork = choice(enemies)
                DropBaby(stork)
        for baby in babies:
            isMoving = baby.ApplyMoveBaby(screen)
            if not isMoving:
                babies.remove(baby)

    def DropBaby(stork):
        baby = Baby(stork.rect, 0, randint(1, 10), "assets/baby.png")
        babies.append(baby)
        screen.blit(baby.image, baby.rect)
        play_sound(down_turn_sound)
        return baby

    if (pygame.mouse.get_pos()[0] - character.rect.x) < 0:
        character.GoToLeft()
    elif (pygame.mouse.get_pos()[0] - character.rect.x) > 0:
        character.GoToRight()

    screen.fill(sky_color)  # === draw _AFTER_ this line ===

    screen.blit(character.image, character.rect)
    for enemy in enemies:
        enemy.Move(screen)
        if enemy.HasExit(screen):
            enemies.remove(enemy)
    
    DropAndMoveBabies()

    for baby in babies:
        isCollide = baby.isCollideBabies(character)
        if isCollide:
            animation = Animation(15)
            animation.animation = lambda: screen.blit(imageInTheBox, pygame.Rect(character.rect.x, character.rect.y-100, 100,100))
            shoot_animations.append(animation)
            babies.remove(baby)
        
    for anim in shoot_animations:
        if not anim.Increment():
            shoot_animations.remove(anim)
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
