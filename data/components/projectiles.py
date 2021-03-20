import pygame
import numpy as np

from pygame.locals import K_1, K_2, K_3
from .base.entity import Entity
from ..setup import graphics_dict
from ..constants import BULLET_VELOCITY

class Bullet(Entity):
    """
    A game's projectile
    """
    def __init__(self, initial_position, direction, weapon_type):
        if weapon_type == K_1:
            super().__init__(initial_position, graphics_dict["bullets"].get_image(32), direction)
        elif weapon_type == K_2:
            super().__init__(initial_position, graphics_dict["bullets"].get_image(39), direction)
        elif weapon_type == K_3:
            super().__init__(initial_position, graphics_dict["bullets"].get_image(48), direction)
        self.velocity = BULLET_VELOCITY
        self.direction = direction

    def update(self):
        """
        Updates the bullet's position.
        """
        d_x = self.velocity * np.cos(np.radians(self.direction))
        d_y = self.velocity * np.sin(np.radians(self.direction))
        self.move(d_x, d_y)

    def draw(self, screen):
        """
        Draws the bullet in game's screen.
        """
        super().draw(screen)


class Projectiles:
    """
    Collection of all current player's bullets in the screen.
    """
    def __init__(self):
        self.projectiles = dict()
        for weapon_type in [K_1, K_2, K_3]:
            self.projectiles[weapon_type] = []

    def add_bullet(self, initial_position, direction, weapon_type):
        """
        Adds a new bullet into projectiles
        """
        self.projectiles[weapon_type].append(Bullet(initial_position, direction, weapon_type))

    def update(self):
        """
        Updates the position of all projectiles
        """
        # TODO : Remove projectiles that are not in the screen anymore
        # TODO : Fix black box around the sprite
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
