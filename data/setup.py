"""
Module that will load sprites, audios and other resources
"""

import pygame

from .components.base.sprite import SpriteSheet
from .constants import BASE_GRAPHICS_DIR, BASE_SOUND_EFFECT_DIR, BASE_SOUNDTRACK_DIR

graphics_dict = {}
sound_dict = {}
music_dict = {}

def load_graphics():
    """
    Loads graphics from archives into the code
    """
    player_graphics = SpriteSheet(BASE_GRAPHICS_DIR + "player.png", (59, 45), 236, 45)
    zombie_graphics = SpriteSheet(BASE_GRAPHICS_DIR + "zombie.png", (45, 45), 90, 45)
    bat_graphics = SpriteSheet(BASE_GRAPHICS_DIR + "bat.png", (64, 64), 256, 64)
    map_graphics = SpriteSheet(BASE_GRAPHICS_DIR + "jawbreaker.png", (8, 8), 64, 72)
    bag_graphics = SpriteSheet(BASE_GRAPHICS_DIR + "bag.png", (102, 84), 102, 84)
    map_night_graphics = SpriteSheet(BASE_GRAPHICS_DIR + "jawbreaker_night.png", (8, 8), 64, 72)
    items_graphics = SpriteSheet(BASE_GRAPHICS_DIR + "items.png", (32, 32), 352, 32)
    bullets_graphics = SpriteSheet(BASE_GRAPHICS_DIR + "firebullet.png", (16, 16), 512, 272)
    status_bar_graphics = SpriteSheet(BASE_GRAPHICS_DIR + "status_bar.png", (800, 100), 800, 100)
    button_graphics = SpriteSheet(BASE_GRAPHICS_DIR + "button.png", (34, 10), 68, 10)
    menu_about_graphics = pygame.image.load(BASE_GRAPHICS_DIR + "menu_about.png")

    title_graphics = [pygame.image.load(BASE_GRAPHICS_DIR + "title_1.png"),
                     pygame.image.load(BASE_GRAPHICS_DIR + "title_2.png"),
                     pygame.image.load(BASE_GRAPHICS_DIR + "title_3.png"),
                     pygame.image.load(BASE_GRAPHICS_DIR + "title_4.png"),
                     pygame.image.load(BASE_GRAPHICS_DIR + "title_5.png")]
    pause_button_graphics = [pygame.transform.scale(pygame.image.load(BASE_GRAPHICS_DIR + "black_pause.png"), (40, 40)),
                             pygame.transform.scale(pygame.image.load(BASE_GRAPHICS_DIR + "white_pause.png"), (40, 40))]
    quit_button_graphics = [pygame.transform.scale(pygame.image.load(BASE_GRAPHICS_DIR + "black_home.png"), (40, 40)),
                            pygame.transform.scale(pygame.image.load(BASE_GRAPHICS_DIR + "white_home.png"), (40, 40))]

    graphics_dict["player"] = player_graphics
    graphics_dict["zombie"] = zombie_graphics
    graphics_dict["bat"] = bat_graphics
    graphics_dict["bag"] = bag_graphics
    graphics_dict["map"] = map_graphics
    graphics_dict["map_night"] = map_night_graphics
    graphics_dict["items"] = items_graphics
    graphics_dict["bullets"] = bullets_graphics
    graphics_dict["status_bar"] = status_bar_graphics
    graphics_dict["title"] = title_graphics
    graphics_dict["button"] = button_graphics
    graphics_dict["about"] = menu_about_graphics
    graphics_dict["pause_button"] = pause_button_graphics
    graphics_dict["quit_button"] = quit_button_graphics

def load_sound():
    """
    Loads sounds from archives into the code
    """
    ak47_sound = pygame.mixer.Sound(BASE_SOUND_EFFECT_DIR + 'ak47.wav')
    uzi_sound = pygame.mixer.Sound(BASE_SOUND_EFFECT_DIR + 'uzi.wav')
    winchester_sound = pygame.mixer.Sound(BASE_SOUND_EFFECT_DIR + 'winchester.wav')
    beep_sound = pygame.mixer.Sound(BASE_SOUND_EFFECT_DIR + 'alert-beep.wav')
    gameover_sound = pygame.mixer.Sound(BASE_SOUND_EFFECT_DIR + 'gameover.wav')
    heartbeat_sound = pygame.mixer.Sound(BASE_SOUND_EFFECT_DIR + 'heartbeat.wav')
    item_sound = pygame.mixer.Sound(BASE_SOUND_EFFECT_DIR + 'item_collect.wav')
    hit_1_sound = pygame.mixer.Sound(BASE_SOUND_EFFECT_DIR + 'hit1.wav')
    menu_select_sound = pygame.mixer.Sound(BASE_SOUND_EFFECT_DIR + 'menu_select.wav')
    monster_scream_sound = pygame.mixer.Sound(BASE_SOUND_EFFECT_DIR + 'monster_scream.wav')
    dying_zombie_sound = pygame.mixer.Sound(BASE_SOUND_EFFECT_DIR + 'dying.wav')
    dying_bat_sound = pygame.mixer.Sound(BASE_SOUND_EFFECT_DIR + 'dying_bat.wav')
    bat_wings_sound = pygame.mixer.Sound(BASE_SOUND_EFFECT_DIR + 'bat_wings.wav')
    heal_sound = pygame.mixer.Sound(BASE_SOUND_EFFECT_DIR + 'heal.wav')
    evil_laugh_sound = pygame.mixer.Sound(BASE_SOUND_EFFECT_DIR + 'evil_laugh.wav')
    ammo_collect_sound = pygame.mixer.Sound(BASE_SOUND_EFFECT_DIR + 'ammo.wav')
    sound_dict['Uzi'] = uzi_sound
    sound_dict['AK47'] = ak47_sound
    sound_dict['Shotgun'] = winchester_sound
    sound_dict['beep'] = beep_sound
    sound_dict['gameover'] = gameover_sound
    sound_dict['heartbeat'] = heartbeat_sound
    sound_dict['item_sound'] = item_sound
    sound_dict['hit_1'] = hit_1_sound
    sound_dict['menu_select'] = menu_select_sound
    sound_dict['monster_scream'] = monster_scream_sound
    sound_dict['dying_zombie'] = dying_zombie_sound
    sound_dict['dying_bat'] = dying_bat_sound
    sound_dict['bat_wings'] = bat_wings_sound
    sound_dict['heal'] = heal_sound
    sound_dict['evil_laugh'] = evil_laugh_sound
    sound_dict['ammo_collect'] = ammo_collect_sound
    sound_dict['Uzi'].set_volume(0.2)
    sound_dict['AK47'].set_volume(0.2)
    sound_dict['Shotgun'].set_volume(0.2)
    sound_dict['gameover'].set_volume(0.5)
    sound_dict['hit_1'].set_volume(0.3)
    sound_dict['heartbeat'].set_volume(1.0)
    sound_dict['menu_select'].set_volume(0.4)
    sound_dict['dying_zombie'].set_volume(0.4)
    sound_dict['dying_bat'].set_volume(0.4)
    sound_dict['bat_wings'].set_volume(0.3)
    sound_dict['monster_scream'].set_volume(0.2)
    sound_dict['heal'].set_volume(0.4)
    sound_dict['item_sound'].set_volume(0.3)
    sound_dict['ammo_collect'].set_volume(0.3)

def load_menu_music():
    """
    Loads menu music from archives into the code
    """
    menu_music = pygame.mixer.music.load(BASE_SOUNDTRACK_DIR + 'horror_game_menu.wav')
