import pygame
import numpy as np

from data.components import player_state
from data.utils import RandomEventGenerator
from . import weapon
from ..constants import PLAYER_INITIAL_HEALTH, BLACK
from ..setup import sound_dict

POTION_TEXT_DURATION = 500
WEAPON_TEXT_DURATION = 1000


class ItemGenerator:
    def __init__(self):
        item_probs = {
            Skull: 0.1,
            Health: 0.2,
            BluePotion: 0.10,
            GreenPotion: 0.10,
            Ammo: 0.50
        }
        self.debuf_generator = RandomEventGenerator(item_probs, null_event=Ammo)

    def generate_item(self):
        item_type = self.debuf_generator.generate()
        item = item_type()
        return item


class Item:
    def __init__(self):
        pass

    def get_sprite(self):
        pass

    def is_potion(self):
        return False

    def apply_effect(self, player, time):
        pass


class Skull(Item):
    def __init__(self):
        super().__init__()

    def get_sprite(self):
        return ITEM_SKULL

    def apply_effect(self, player, time):
        player.state.send_event(player_state.STRONGER_EVENT, time)
        sound_dict['evil_laugh'].play()


class Health(Item):
    def __init__(self):
        super().__init__()

    def get_sprite(self):
        return ITEM_HEALTH

    def is_potion(self):
        return True

    def apply_effect(self, player, time):
        player.health = min(player.health + 1, PLAYER_INITIAL_HEALTH)
        # Write in screen
        text = '+ HEALTH'
        player.write(text, time, WEAPON_TEXT_DURATION)
        sound_dict['heal'].play()


class BluePotion(Item):
    def __init__(self):
        super().__init__()

    def get_sprite(self):
        return ITEM_BLUEPOTION

    def is_potion(self):
        return True

    def apply_effect(self, player, time):
        player.state.send_event(player_state.STOP_BLEEDING_EVENT, time)
        # Write in screen
        text = 'STOP BLEEDING'
        player.write(text, time, WEAPON_TEXT_DURATION)
        sound_dict['heal'].play()


class GreenPotion(Item):
    def __init__(self):
        super().__init__()

    def get_sprite(self):
        return ITEM_GREENPOTION

    def is_potion(self):
        return True

    def apply_effect(self, player, time):
        player.state.send_event(player_state.STOP_SLOW_EVENT, time)
        # Write in screen
        text = 'STOP SLOW'
        player.write(text, time, WEAPON_TEXT_DURATION)
        sound_dict['heal'].play()


class Ammo(Item):
    def __init__(self):
        super().__init__()

    def get_sprite(self):
        return ITEM_AMMO

    def apply_effect(self, player, time):
        weapon_probs = {}
        prob = 1.0 / len(player.weapons)
        for weapon in player.weapons.values():
            weapon_probs[weapon] = prob
        weapon = RandomEventGenerator(weapon_probs, null_event=player.weapons[player.current_weapon_name]).generate()

        # Generate ammo
        gen_ammo = int(weapon.max_ammo / 5)
        player.bullets[weapon.name] = min(weapon.max_ammo, player.bullets[weapon.name] + gen_ammo)
        player.update_ammo()

        # Write in screen
        text = '+' + str(gen_ammo) + ' ' + weapon.name
        player.write(text, time, WEAPON_TEXT_DURATION)
        sound_dict['ammo_collect'].play()



ITEM_SKULL = 90
ITEM_HEALTH = 91
ITEM_BLUEPOTION = 92
ITEM_GREENPOTION = 93
ITEM_AMMO = 94