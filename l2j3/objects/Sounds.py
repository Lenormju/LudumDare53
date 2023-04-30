import pygame

pygame.mixer.init()

num_channels = pygame.mixer.get_num_channels()

BACKGROUND_MUSIC_CHANNEL_ID = 0
pygame.mixer.set_reserved(BACKGROUND_MUSIC_CHANNEL_ID)
background_music_channel = pygame.mixer.Channel(BACKGROUND_MUSIC_CHANNEL_ID)

def play_music(music):
    background_music_channel.play(music)
    background_music_channel.set_volume(1)

def play_music_next(music):
    background_music_channel.queue(music)

def play_sound(sound):
    a_sound_channel = pygame.mixer.find_channel(force=False)
    if a_sound_channel is not None:
        a_sound_channel.play(sound)
        a_sound_channel.set_volume(0.2)

bomb_sound = pygame.mixer.Sound("assets/bomb.mp3")
good_box_sound = pygame.mixer.Sound("assets/positif.mp3")
bad_box_sound = pygame.mixer.Sound("assets/negatif.mp3")
miss_box_sound = pygame.mixer.Sound("assets/splortsh.mp3")
shoot_sound = pygame.mixer.Sound("assets/shoot.mp3")
prout_sound = pygame.mixer.Sound("assets/prout.mp3")
baby_sound = pygame.mixer.Sound("assets/baby.mp3")
boss_stork_sound = pygame.mixer.Sound("assets/boss_cygogne.mp3")
explosion_sound = pygame.mixer.Sound("assets/explosion.mp3")

birds_music = pygame.mixer.Sound("assets/birds.mp3")
nyan_music = pygame.mixer.Sound("assets/nyan.mp3")
martial_music = pygame.mixer.Sound("assets/martial.mp3")
metal_bad2_music = pygame.mixer.Sound("assets/metal_v2.mp3")
