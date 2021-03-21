"""
Entity that is an enemy to the player,
programmed to stalk and hurt him
"""

import numpy as np
from ..base.entity import Entity
from ...constants import DEFAULT_ENEMY_VELOCITY, DEFAULT_ENEMY_HEALTH
from ...constants import DEFAULT_ENEMY_DAMAGE, FRAMES_TO_ENEMIES_TURN
from ...constants import FRAMES_PER_SECOND

class Enemy(Entity):
    """
    Abstraction of a stalker enemy
    """
    def __init__(self, position, sprite_graphic):
        super().__init__(position, sprite_graphic)
        self.health = DEFAULT_ENEMY_HEALTH
        self.velocity = DEFAULT_ENEMY_VELOCITY*FRAMES_TO_ENEMIES_TURN
        self.damage = DEFAULT_ENEMY_DAMAGE

        self.previous_pos = position
        self.curr_pos = position
        self.looking_angle = 0

    def estimate_velocity(self):
        """
        Obtains an estimate of enemy velocity
        by finite differences
        """
        return (np.array(self.curr_pos) - np.array(self.previous_pos))*FRAMES_PER_SECOND/FRAMES_TO_ENEMIES_TURN

    def ai_move(self, target): # TODO: it only goes in the direction of target, should be smarter
        """
        Function responsible for making the enemy go towards
        the player
        param target: where it should go, supposedly the player position
        type target: numpy array
        """
        self.previous_pos = self.curr_pos
        self.curr_pos = self.get_position()

        diff = target - self.get_position()

        diff = diff/np.linalg.norm(diff)
        self.move(diff[0]*self.velocity, diff[1]*self.velocity)

        velocity_vector = self.estimate_velocity()
        if np.linalg.norm(velocity_vector):
            self.looking_angle = -np.degrees(np.arctan2(velocity_vector[1], velocity_vector[0]))
