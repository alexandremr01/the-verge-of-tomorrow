import pygame
import numpy as np

from pygame.locals import K_1, K_2, K_3
from .base.entity import Entity
from ..setup import graphics_dict
from ..constants import BULLET_VELOCITY, SCREEN_WIDTH, SCREEN_HEIGHT

class Bullet(Entity):
    """
    A game's projectile
    """
    def __init__(self, initial_position, weapon_position, direction, weapon_type):
        if weapon_type == K_1:
            super().__init__(initial_position, graphics_dict["bullets"].get_image(32), direction)
        elif weapon_type == K_2:
            super().__init__(initial_position, graphics_dict["bullets"].get_image(39), direction)
        elif weapon_type == K_3:
            super().__init__(initial_position, graphics_dict["bullets"].get_image(48), direction)
        self.velocity = BULLET_VELOCITY
        self.direction = direction
        self.screen_position = [SCREEN_WIDTH // 2 + int(weapon_position[0]), 
                                SCREEN_HEIGHT // 2 + int(weapon_position[1])]

    def update(self):
        """
        Updates the bullet's position.
        """
        d_x = self.velocity * np.cos(np.radians(self.direction))
        d_y = self.velocity * np.sin(np.radians(self.direction))
        self.screen_position[0] += int(d_x)
        self.screen_position[1] += int(d_y)
        self.move(d_x, d_y)

    def draw(self, screen):
        """
        Draws the bullet in game's screen.
        """
        super().draw(screen)

    def is_visible(self):
        """
        Verifies if the bullet is visible in the screen.
        """
        threshold = 16
        if -threshold < self.screen_position[0] < SCREEN_WIDTH + threshold:
            if -threshold < self.screen_position[1] < SCREEN_HEIGHT + threshold:
                return True
        return False


class Projectiles:
    """
    Collection of all current player's bullets in the screen.
    """
    def __init__(self):
        self.projectiles = dict()
        for weapon_type in [K_1, K_2, K_3]:
            self.projectiles[weapon_type] = []

    def add_bullet(self, initial_position, weapon_position, direction, weapon_type):
        """
        Adds a new bullet into projectiles
        """
        self.projectiles[weapon_type].append(Bullet(initial_position, weapon_position, 
                                                    direction, weapon_type))

    def update(self):
        """
        Updates the position of all projectiles
        """
        for key in self.projectiles.keys():
            self.projectiles[key] = [bullet for bullet in self.projectiles[key] 
                                     if bullet.is_visible()]
        for key in self.projectiles.keys():
            for bullet in self.projectiles[key]:
                bullet.update()
        
    def draw(self, screen):
        """
        Draws all visible projectiles
        """
        for key in self.projectiles.keys():
            for bullet in self.projectiles[key]:
                bullet.draw(screen)
