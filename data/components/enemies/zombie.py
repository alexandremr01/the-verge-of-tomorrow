"""
Enemy most common in the game
"""

import numpy as np

from .enemy import Enemy
from ...constants import ZOMBIE_HEALTH, ZOMBIE_VELOCITY, ZOMBIE_DAMAGE, EPSILON, FRAMES_TO_ENEMIES_TURN
from ...setup import graphics_dict

class Zombie(Enemy):
    """
    Common enemy, with common atributes
    """
    def __init__(self, position):
        super().__init__(position, graphics_dict["zombie"].get_image(0))
        self.health = ZOMBIE_HEALTH
        self.velocity = ZOMBIE_VELOCITY*FRAMES_TO_ENEMIES_TURN
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
