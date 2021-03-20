"""
Enemy most common in the game
"""

from .enemy import Enemy
from ...constants import ZOMBIE_HEALTH, ZOMBIE_VELOCITY, EPSILON
from ...setup import graphics_dict

class Zombie(Enemy):
    """
    Common enemy, with common atributes
    """
    def __init__(self, position):
        super().__init__(position, graphics_dict["zombie"].get_image(0))
        self.health = ZOMBIE_HEALTH
        self.velocity = ZOMBIE_VELOCITY

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
        if self.estimate_velocity() > EPSILON:
            self.update_sprite(graphics_dict["zombie"].get_image(1))
        else:
            self.update_sprite(graphics_dict["zombie"].get_image(0))
        super().draw(screen)
