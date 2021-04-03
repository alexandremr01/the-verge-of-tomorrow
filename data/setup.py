"""
Module that will load sprites, audios and other resources
"""

import pygame

from .components.base.sprite import SpriteSheet
from .constants import BASE_GRAPHICS_DIR, BASE_SOUND_DIR, BASE_MUSIC_DIR

graphics_dict = {}
sound_dict = {}

def load_graphics():
    """
    Loads graphics from archives into the code
    """
    player_graphics = SpriteSheet(BASE_GRAPHICS_DIR + "player.png", (59, 45), 236, 45)
    zombie_graphics = SpriteSheet(BASE_GRAPHICS_DIR + "zombie.png", (45, 45), 90, 45)
    map_graphics = SpriteSheet(BASE_GRAPHICS_DIR + "jawbreaker.png", (8, 8), 64, 72)
    items_graphics = SpriteSheet(BASE_GRAPHICS_DIR + "items.png", (32, 32), 352, 32)
    bullets_graphics = SpriteSheet(BASE_GRAPHICS_DIR + "firebullet.png", (16, 16), 512, 272)
    status_bar_graphics = SpriteSheet(BASE_GRAPHICS_DIR + "status_bar.png", (800, 100), 800, 100)
    graphics_dict["player"] = player_graphics
    graphics_dict["zombie"] = zombie_graphics
    graphics_dict["map"] = map_graphics
    graphics_dict["items"] = items_graphics
    graphics_dict["bullets"] = bullets_graphics
    graphics_dict["status_bar"] = status_bar_graphics

def load_sound():
    """
    Loads sounds from archives into the code
    """
    ak47_sound = pygame.mixer.Sound(BASE_SOUND_DIR + 'ak47.wav')
    uzi_sound = pygame.mixer.Sound(BASE_SOUND_DIR + 'uzi.wav')
    winchester_sound = pygame.mixer.Sound(BASE_SOUND_DIR + 'winchester.wav')
    beep_sound = pygame.mixer.Sound(BASE_SOUND_DIR + 'alert-beep.wav')
    gameover_sound = pygame.mixer.Sound(BASE_SOUND_DIR + 'gameover.wav')
    heartbeat_sound = pygame.mixer.Sound(BASE_SOUND_DIR + 'heartbeat.wav')
    item_sound = pygame.mixer.Sound(BASE_SOUND_DIR + 'item_collect.wav')
    sound_dict['WEAPON_K_1'] = uzi_sound
    sound_dict['WEAPON_K_2'] = ak47_sound
    sound_dict['WEAPON_K_3'] = winchester_sound
    sound_dict['beep'] = beep_sound
    sound_dict['gameover'] = gameover_sound
    sound_dict['heartbeat'] = heartbeat_sound
    sound_dict['item_sound'] = item_sound
    sound_dict['WEAPON_K_1'].set_volume(0.2)
    sound_dict['WEAPON_K_2'].set_volume(0.2)
    sound_dict['WEAPON_K_3'].set_volume(0.2)
