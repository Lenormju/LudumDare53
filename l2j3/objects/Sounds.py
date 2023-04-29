import pygame

pygame.mixer.init()

background_sound = pygame.mixer.Sound(r'sound/AMBForst_Foret (ID 0100)_LS.wav')
left_turn_sound = pygame.mixer.Sound(r'assets/left_turn.mp3')
right_turn_sound = pygame.mixer.Sound(r'assets/right_turn.mp3')
down_turn_sound = pygame.mixer.Sound(r'assets/down_turn.mp3')
explosion_sound = pygame.mixer.Sound(r'assets/explosion.mp3')
