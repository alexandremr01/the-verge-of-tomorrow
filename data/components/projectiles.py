import pygame
import numpy as np

from .base.entity import Entity
from ..setup import graphics_dict
from ..constants import (BULLET_VELOCITY, SCREEN_WIDTH, SCREEN_HEIGHT)
from data.components.weapon import Uzi, Shotgun, AK47
class Bullet(Entity):
    """
    A game's projectile
    """
    def __init__(self, initial_position, weapon_position, direction, weapon, damage=None):
        super().__init__(initial_position, graphics_dict["bullets"].get_image(weapon.get_bullet_image_index()), direction)
        if damage is None:
            self.damage = weapon.get_damage()
        else:
            self.damage = damage
        self.velocity = BULLET_VELOCITY
        self.direction = direction
        self.screen_position = [SCREEN_WIDTH // 2 + int(weapon_position[0]), 
                                SCREEN_HEIGHT // 2 + int(weapon_position[1])]

    def get_damage(self):
        """
        Returns bullet damage.
        """
        return self.damage

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
        threshold = 200
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
        for weapon_name in ["Uzi", "Shotgun", "AK47"]:
            self.projectiles[weapon_name] = []

    def add_bullet(self, initial_position, weapon_position, direction, weapon, damage):
        """
        Adds a new bullet into projectiles
        """
        self.projectiles[weapon.get_name()].append(Bullet(initial_position, weapon_position, 
                                                    direction, weapon, damage))

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

    def handle_collision(self, enemy):
        """
        Handles collisions between enemy and any projectile.
        """
        for key in self.projectiles.keys():
            num_bullets = len(self.projectiles[key])
            if num_bullets == 0:
                continue
            collided_bullets = [bullet for bullet in self.projectiles[key]
                                if pygame.sprite.collide_rect(
                    bullet.get_sprite(), enemy.get_sprite())]
            damage = np.sum([bullet.damage for bullet in collided_bullets])
            enemy.hurt(damage)
            self.projectiles[key] = [bullet for bullet in self.projectiles[key]
                                     if not pygame.sprite.collide_rect(
                                     bullet.get_sprite(), enemy.get_sprite())]

