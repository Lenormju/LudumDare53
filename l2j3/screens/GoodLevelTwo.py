import pygame

from GameInfo import GAME_INFO, GameScreen
from objects.Stork import Stork
from objects.Unicorn import Unicorn
from objects.Direction import Direction
from objects.Character import Character
from objects.Sounds import background_sound, explosion_sound
from objects.Animation import Animation
from objects.Sounds import down_turn_sound
from objects.Shoot import Shoot
from objects.Baby import Baby
from objects.Colors import *
from random import *

background_sound.play(loops=-1)

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
unicorn_image = pygame.image.load("assets/unicorn.png")
enemies.append(Unicorn(unicorn_image,
                    Direction.RIGHT,
                    randint(0, 0),
                    randint(0, GAME_INFO.SCREEN_HEIGHT/2)))

character = Character(pygame.Rect(GAME_INFO.SCREEN_WIDTH/2, GAME_INFO.SCREEN_HEIGHT-100, 100, 100), 10, "assets/panier.png")
player_has_lost = False
firstTick = True

shoot_animations = []
start_ticks = 0

def render(screen, events, keys):
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
            if GAME_INFO.SCORE > 15:
                ClearBoard(GameScreen.GOOD_ENDING)
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
        if GAME_INFO.CURRENT_TICK_NUMBER % randint(30, 90) == 0:
            if enemies:
                enemy = choice(enemies)
                DropBaby(enemy)
        for baby in babies:
            isMoving = baby.ApplyMoveBaby(screen)
            if not isMoving:
                babies.remove(baby)

    def DropBaby(enemy):
        baby = Baby(enemy.rect, randint(1, 10), enemy.baby_picture_path)
        babies.append(baby)
        screen.blit(baby.image, baby.rect)
        pygame.mixer.find_channel(force=True).play(down_turn_sound)
        return baby

    shooting = False

    if keys[pygame.K_LEFT]:
        character.GoToLeft()
    if keys[pygame.K_RIGHT]:
        character.GoToRight()

    # for event in events:
    #     if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
    #         shooting = True

    screen.fill(sky_color)  # === draw _AFTER_ this line ===

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
    ColoredTextEnd((0,0,0), "Score : "+str(GAME_INFO.SCORE), GAME_INFO.SCREEN_WIDTH-150, 0)
    ColoredTextEnd((0,0,0), "Timer : "+str(round(seconds)), GAME_INFO.SCREEN_WIDTH/3, 0)

    # check if alien destroys the player
    for enemy in enemies:
        if enemy.rect.colliderect(character.rect):
            explosion_sound.play()
            player_has_lost = True
            break

    DetermineEndGame()
