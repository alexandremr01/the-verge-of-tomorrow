"""
Entity that is an enemy to the player,
programmed to stalk and hurt him
"""

import numpy as np
from ..base.entity import Entity
from ...constants import DEFAULT_ENEMY_VELOCITY, DEFAULT_ENEMY_HEALTH

class Enemy(Entity):
    """
    Abstraction of a stalker enemy
    """
    def __init__(self, position, sprite_graphic):
        super().__init__(position, sprite_graphic)
        self.health = DEFAULT_ENEMY_HEALTH
        self.velocity = DEFAULT_ENEMY_VELOCITY

    def ai_move(self, target):
        """
        Function responsible for making the enemy go towards
        the player
        param target: where it should go, supposedly the player position
        type target: numpy array
        """
        curr = np.array(self.get_position())
        diff = target - curr
        diff = diff/np.linalg.norm(diff)
        self.move(diff[0]*self.velocity, diff[1]*self.velocity)
