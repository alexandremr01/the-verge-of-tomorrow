"""
Enemy most common in the game
"""

import numpy as np

from .enemy import Enemy
from ...constants import ZOMBIE_HEALTH, ZOMBIE_VELOCITY, ZOMBIE_DAMAGE, ZOMBIE_SCORE 
from ...constants import ZOMBIE_NOISE_INTERVAL, PLAYER_HEAR_DISTANCE
from ...constants import FRAMES_TO_ENEMIES_TURN, EPSILON
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
        self.last_noise_time = 0

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

    def play_noise(self, time, player_position):
        """
        Plays a zombie grunt sfx
        """
        if np.linalg.norm(player_position - self.get_position()) < PLAYER_HEAR_DISTANCE:
            if time - self.last_noise_time > ZOMBIE_NOISE_INTERVAL:
                self.last_noise_time = time
                sound_dict['monster_scream'].play()
