"""
Enemy most common in the game
"""

from .enemy import Enemy
from ...constants import ZOMBIE_HEALTH, ZOMBIE_VELOCITY
from ...setup import graphics_dict

class Zombie(Enemy):
    """
    Common enemy, with common atributes
    """
    def __init__(self, position):
        super().__init__(position, graphics_dict["test_sprite"]) # TODO: use zombie sprite
        self.health = ZOMBIE_HEALTH
        self.velocity = ZOMBIE_VELOCITY
