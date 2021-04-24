"""
Entity that is an enemy to the player,
programmed to stalk and hurt him
"""

from math import sin, cos, pi
import numpy as np
from ..base.entity import Entity
from ...constants import DEFAULT_ENEMY_VELOCITY, DEFAULT_ENEMY_HEALTH
from ...constants import DEFAULT_ENEMY_DAMAGE, FRAMES_TO_ENEMIES_TURN
from ...constants import FRAMES_PER_SECOND, OBJECT_REPULSION, PREDICTION_LEN
from ...constants import PREDICTION_STEP, TIME_TO_PREDICT

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
        step = -15*pi/180
        self.clock_rot_mat = np.array([[cos(step), -sin(step)], [sin(step), cos(step)]])
        self.counter_rot_mat = np.array([[cos(-step), -sin(-step)], [sin(-step), cos(-step)]])
        self.frame = 0
        self.clockwise = True

    def estimate_velocity(self):
        """
        Obtains an estimate of enemy velocity
        by finite differences
        """
        return (np.array(self.curr_pos) - np.array(self.previous_pos))*FRAMES_PER_SECOND/FRAMES_TO_ENEMIES_TURN

    def search_valid_direction(self, diff, validate_pos, clock):
        """
        Searches a direction to move to
        """
        iteration = 0
        while not validate_pos(self.curr_pos + diff*OBJECT_REPULSION) and iteration < 36:
            if clock:
                diff = self.clock_rot_mat.dot(diff)
            else:
                diff = self.counter_rot_mat.dot(diff)

            iteration += 1

        return diff

    def predict(self, target, validate_pos, clock):
        """
        Predicts its future state using either a clockwise
        greedy path planning or a counter clockwise greedy
        path planning
        """
        predicted_pos = self.get_position()

        iteration = 0
        while iteration < PREDICTION_LEN and np.linalg.norm(target - predicted_pos) > PREDICTION_STEP/2:
            diff = target - predicted_pos
            diff = diff/np.linalg.norm(diff)
            diff = self.search_valid_direction(diff, validate_pos, clock)
            predicted_pos = predicted_pos + diff*PREDICTION_STEP

            iteration += 1

        return iteration, np.linalg.norm(target - predicted_pos)

    def ai_move(self, target, validate_pos):
        """
        Default trajectory planning for a enemy
        It stays in idle (random) movement if not near
        the player. Otherwise, it follows a greedy
        path planning algorithm
        """
        self.previous_pos = self.curr_pos
        self.curr_pos = self.get_position()
        self.frame += 1

        if self.frame > TIME_TO_PREDICT:
            self.frame = 0
            self.clockwise = True

            iteration_clockwise, dist_clockwise = self.predict(target, validate_pos, True)
            iteration_counter, dist_counter = self.predict(target, validate_pos, False)

            if iteration_clockwise == iteration_counter:
                if dist_counter < dist_clockwise:
                    self.clockwise = False
            elif iteration_counter < iteration_clockwise:
                self.clockwise = False

        diff = target - self.get_position()

        diff = diff/np.linalg.norm(diff)
        diff = self.search_valid_direction(diff, validate_pos, self.clockwise)
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
