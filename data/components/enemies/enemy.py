"""
Entity that is an enemy to the player,
programmed to stalk and hurt him
"""

import numpy as np
from ..base.entity import Entity
from ...constants import DEFAULT_ENEMY_VELOCITY, DEFAULT_ENEMY_HEALTH
from ...constants import FRAMES_PER_SECOND

class Enemy(Entity):
    """
    Abstraction of a stalker enemy
    """
    def __init__(self, position, sprite_graphic):
        super().__init__(position, sprite_graphic)
        self.health = DEFAULT_ENEMY_HEALTH
        self.velocity = DEFAULT_ENEMY_VELOCITY

        self.previous_pos = None
        self.curr_pos = position

    def estimate_velocity(self):
        """
        Obtains an estimate of enemy velocity
        by finite differences
        """
        if self.previous_pos is None:
            return self.velocity

        velocity = (np.array(self.curr_pos) - np.array(self.previous_pos))*FRAMES_PER_SECOND
        return np.linalg.norm(velocity)

    def ai_move(self, target): # TODO: it only goes in the direction of target, should be smarter
        """
        Function responsible for making the enemy go towards
        the player
        param target: where it should go, supposedly the player position
        type target: numpy array
        """
        diff = target - self.get_position()

        diff = diff/np.linalg.norm(diff)
        self.move(diff[0]*self.velocity, diff[1]*self.velocity)

    def draw(self, screen):
        """
        Draws zombie on screen, updating
        params to estimate its velocity
        """
        self.previous_pos = self.curr_pos
        self.curr_pos = self.get_position()

        super().draw(screen)
