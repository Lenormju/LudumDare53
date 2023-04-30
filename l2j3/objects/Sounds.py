import pygame

pygame.mixer.init()

num_channels = pygame.mixer.get_num_channels()

BACKGROUND_MUSIC_CHANNEL_ID = 0
pygame.mixer.set_reserved(BACKGROUND_MUSIC_CHANNEL_ID)
background_music_channel = pygame.mixer.Channel(BACKGROUND_MUSIC_CHANNEL_ID)

def play_music(music):
    background_music_channel.play(music)
    background_music_channel.set_volume(1)

def play_sound(sound):
    a_sound_channel = pygame.mixer.find_channel(force=False)
    if a_sound_channel is not None:
        a_sound_channel.play(sound)
        a_sound_channel.set_volume(0.2)

left_turn_sound = pygame.mixer.Sound(r'assets/left_turn.mp3')
right_turn_sound = pygame.mixer.Sound(r'assets/right_turn.mp3')
down_turn_sound = pygame.mixer.Sound(r'assets/down_turn.mp3')
explosion_sound = pygame.mixer.Sound(r'assets/explosion.mp3')
metal_bad2_music = pygame.mixer.Sound("assets/metal_v1.mp3")
