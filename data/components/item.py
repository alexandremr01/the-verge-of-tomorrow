from data.components import player_state
from data.utils import RandomEventGenerator
from . import weapon
import pygame
import numpy as np
from ..constants import PLAYER_INITIAL_HEALTH, BLACK

class ItemGenerator:
    def __init__(self):
        item_probs = {
            # Skull: 0.1,
            # Health: 0.1,
            # BluePotion: 0.30,
            # GreenPotion: 0.30,
            Ammo: 0.9
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

    def apply_effect(self, player, time):
        pass


class Skull(Item):
    def __init__(self):
        super().__init__()

    def get_sprite(self):
        return "ITEM_SKULL"

    def apply_effect(self, player, time):
        player.state.send_event(player_state.STRONGER_EVENT, time)


class Health(Item):
    def __init__(self):
        super().__init__()

    def get_sprite(self):
        return "ITEM_HEALTH"

    def apply_effect(self, player, time):
        player.health = min(player.health + 1, PLAYER_INITIAL_HEALTH)


class BluePotion(Item):
    def __init__(self):
        super().__init__()

    def get_sprite(self):
        return "ITEM_BLUEPOTION"

    def apply_effect(self, player, time):
        player.state.send_event(player_state.STOP_BLEEDING_EVENT, time)


class GreenPotion(Item):
    def __init__(self):
        super().__init__()

    def get_sprite(self):
        return "ITEM_GREENPOTION"

    def apply_effect(self, player, time):
        player.state.send_event(player_state.STOP_SLOW_EVENT, time)

WEAPON_TEXT_DURATION = 1000
class Ammo(Item):
    def __init__(self):
        super().__init__()

    def get_sprite(self):
        return "ITEM_AMMO"

    def apply_effect(self, player, time): # TODO: write weapon on screen
        weapon_probs = {}
        prob = 1.0 / len(player.weapons)
        for weapon in player.weapons.values():
            weapon_probs[weapon] = prob
        weapon = RandomEventGenerator(weapon_probs, null_event=player.weapons[player.current_weapon_name]).generate()

        # Write in screen
        player.write(weapon.name, time, WEAPON_TEXT_DURATION)

        # Generate ammo
        new_ammo = player.bullets[weapon.name] + weapon.max_ammo / 5
        player.bullets[weapon.name] = int(np.floor(min(weapon.max_ammo, new_ammo)))
        player.update_ammo()

