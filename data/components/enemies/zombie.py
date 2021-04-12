"""
Enemy most common in the game
"""

from math import pi, cos, sin
import numpy as np

from .enemy import Enemy
from ...constants import ZOMBIE_HEALTH, ZOMBIE_VELOCITY, ZOMBIE_DAMAGE, ZOMBIE_SCORE
from ...constants import EPSILON, FRAMES_TO_ENEMIES_TURN, EPSILON
from ...setup import graphics_dict, sound_dict

class Zombie(Enemy):
    """
    Common enemy, with common atributes
    """
    def __init__(self, position):
        super().__init__(position, graphics_dict["zombie"].get_image(0))
        self.health = ZOMBIE_HEALTH
        self.velocity = ZOMBIE_VELOCITY*FRAMES_TO_ENEMIES_TURN
        self.score = ZOMBIE_SCORE
        self.looking_angle = 0
        self.damage = ZOMBIE_DAMAGE

    def get_damage(self):
        """
        Returns zombie's damage.
        """
        return self.damage

    def hurt(self, damage):
        """
        Decreases zombie health by damage
        """
        self.health = self.health - damage
        if self.health < 0:
            self.health = 0
            sound_dict['dying_zombie'].play()

    def draw(self, screen):
        """
        Draws the zombie sprite in a dynamic way
        in order to create animation
        """
        velocity_vector = self.estimate_velocity()
        if np.linalg.norm(velocity_vector) > EPSILON:
            self.update_sprite(graphics_dict["zombie"].get_image(1), self.looking_angle)
        else:
            self.update_sprite(graphics_dict["zombie"].get_image(0), self.looking_angle)
        super().draw(screen)

    def clockwise_move(self, diff, validate_pos):
        """
        Movement vector is planned clockwise
        """
        step = -5*pi/180
        rotation_matrix = np.array([[cos(step), -sin(step)], [sin(step), cos(step)]])
        while not validate_pos(self.curr_pos + diff*self.velocity):
            diff = rotation_matrix.dot(diff)

        return diff

    def ai_move(self, target, validate_pos):
        """
        Trajectory planning for zombie
        """
        self.previous_pos = self.curr_pos
        self.curr_pos = self.get_position()

        diff = target - self.get_position()

        diff = diff/np.linalg.norm(diff)
        diff = self.clockwise_move(diff, validate_pos)
        self.move(diff[0]*self.velocity, diff[1]*self.velocity)

        velocity_vector = self.estimate_velocity()
        if np.linalg.norm(velocity_vector):
            self.looking_angle = -np.degrees(np.arctan2(velocity_vector[1], velocity_vector[0]))
