"""
Entity that is an enemy to the player,
programmed to stalk and hurt him
"""

from math import sin, cos, pi
import numpy as np
from ..base.entity import Entity
from ...constants import DEFAULT_ENEMY_VELOCITY, DEFAULT_ENEMY_HEALTH
from ...constants import DEFAULT_ENEMY_DAMAGE, FRAMES_TO_ENEMIES_TURN
from ...constants import FRAMES_PER_SECOND, PREDICTION_STEP, VALID_POS_SEARCH_STEP

class Enemy(Entity):
    """
    Abstraction of a stalker enemy
    """
    def __init__(self, position, sprite_graphic):
        super().__init__(position, sprite_graphic)
        self.health = DEFAULT_ENEMY_HEALTH
        self.velocity = DEFAULT_ENEMY_VELOCITY*FRAMES_TO_ENEMIES_TURN
        self.damage = DEFAULT_ENEMY_DAMAGE
        self.flying = False

        self.previous_pos = position
        self.curr_pos = position
        self.looking_angle = 0
        step = -VALID_POS_SEARCH_STEP*pi/180
        self.clock_rot_mat = np.array([[cos(step), -sin(step)], [sin(step), cos(step)]])
        self.counter_rot_mat = np.array([[cos(-step), -sin(-step)], [sin(-step), cos(-step)]])

    def estimate_velocity(self):
        """
        Obtains an estimate of enemy velocity
        by finite differences
        """
        return (np.array(self.curr_pos) - np.array(self.previous_pos))*FRAMES_PER_SECOND/FRAMES_TO_ENEMIES_TURN

    def search_valid_direction(self, diff, validate_pos):
        """
        Searches a direction to move to
        """
        iteration = 0
        max_iterations = 360/VALID_POS_SEARCH_STEP
        while validate_pos(self.curr_pos + diff*(self.sprite.get_width()/2 + PREDICTION_STEP)) and iteration < max_iterations:
            diff = self.counter_rot_mat.dot(diff)

            iteration += 1

        return diff

    def ai_move(self, target, validate_pos):
        """
        Default trajectory planning for a enemy
        It stays in idle (random) movement if not near
        the player. Otherwise, it follows a greedy
        path planning algorithm
        """
        self.previous_pos = self.curr_pos
        self.curr_pos = self.get_position()

        diff = target - self.get_position()
        diff = diff/np.linalg.norm(diff)

        diff = self.search_valid_direction(diff, validate_pos)
        self.move(diff[0]*self.velocity, diff[1]*self.velocity)

        velocity_vector = self.estimate_velocity()
        if np.linalg.norm(velocity_vector):
            self.looking_angle = -np.degrees(np.arctan2(velocity_vector[1], velocity_vector[0]))

    def play_noise(self, time, player_position):
        """
        Plays the enemy's noise sound effect.
        This is an abstract method.
        """
        pass
