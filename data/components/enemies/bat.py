"""
Fast, flying enemy
"""

import numpy as np

from .enemy import Enemy
from ...constants import BAT_HEALTH, BAT_VELOCITY, BAT_DAMAGE, BAT_WING_FREQUENCY, BAT_SCORE, BAT_NOISE_INTERVAL
from ...constants import FRAMES_TO_ENEMIES_TURN, PLAYER_HEAR_DISTANCE
from ...setup import graphics_dict, sound_dict

class Bat(Enemy):
    """
    Enemy, with low damage, but is fast and bypasses obstacles
    """
    def __init__(self, position):
        super().__init__(position, graphics_dict["bat"].get_image(0))
        self.health = BAT_HEALTH
        self.velocity = BAT_VELOCITY*FRAMES_TO_ENEMIES_TURN
        self.score = BAT_SCORE
        self.looking_angle = 0
        self.damage = BAT_DAMAGE
        self.flying = True
        self.flying_pose = 0
        self.frame = 0
        self.last_noise_time = 0

    def get_damage(self):
        """
        Returns bat's damage.
        """
        return self.damage

    def hurt(self, damage):
        """
        Decreases bat health by damage
        """
        self.health = self.health - damage
        if self.health < 0:
            self.health = 0
            sound_dict['dying_bat'].play()

    def draw(self, screen):
        """
        Draws the bat's sprite in a dynamic way
        in order to create animation
        """
        self.frame += 1
        if self.frame >= BAT_WING_FREQUENCY:
            self.flying_pose += 1
            self.flying_pose %= 4
            self.frame = 0
        self.update_sprite(graphics_dict["bat"].get_image(self.flying_pose), self.looking_angle - 90)
        super().draw(screen)

    def ai_move(self, target, validate_pos):
        """
        Trajectory planner for bat
        It goes over structures, so it simply follows the
        straigth line between itself and the player, coupled
        with a flying effect in the form of a MHS
        """
        self.previous_pos = self.curr_pos
        self.curr_pos = self.get_position()

        diff = target - self.get_position()

        diff = diff/np.linalg.norm(diff)
        self.move(diff[0]*self.velocity, diff[1]*self.velocity)

        velocity_vector = self.estimate_velocity()
        if np.linalg.norm(velocity_vector):
            self.looking_angle = -np.degrees(np.arctan2(velocity_vector[1], velocity_vector[0]))

    def play_noise(self, time, player_position):
        """
        Plays a bat's wings sfx
        """
        if np.linalg.norm(player_position - self.get_position()) < PLAYER_HEAR_DISTANCE:
            if time - self.last_noise_time >= BAT_NOISE_INTERVAL:
                self.last_noise_time = time
                sound_dict['bat_wings'].play()