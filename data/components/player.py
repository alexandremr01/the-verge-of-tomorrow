"""
Module containing player related abstractions.
The player being controlled by the user.
"""

import pygame
import numpy as np
from pygame.locals import K_1, K_2, K_3, K_w, K_a, K_s, K_d

from ..constants import MAP_WIDTH, MAP_HEIGHT
from ..setup import graphics_dict
from .base.entity import Entity


class Hud():
    """
    Heads-up display containing player's status and score.
    """
    def __init__(self, max_health, items_graphics):
        self.heart = [True] * max_health
        self.heart_sprites = [items_graphics.get_image(4), items_graphics.get_image(5)]
        self.heart_positions = [(20+35*i, 20) for i in range(max_health)]
        self.current_weapon = 0
        self.weapon_sprites = [pygame.transform.scale(items_graphics.get_image(7), (90, 90)),
                               pygame.transform.scale(items_graphics.get_image(6), (90, 90)), 
                               pygame.transform.scale(items_graphics.get_image(8), (90, 90))]
        self.weapon_position = (650, 700)

    def update(self, key, health=None): # TODO: include score and status
        """
        Updates all the hud's elements
        """
        if key == K_1:
            self.current_weapon = 0
        elif key == K_2:
            self.current_weapon = 1
        elif key == K_3:
            self.current_weapon = 2
        if health is not None:
            self.heart[health:] = [False] * len(self.heart[health:])

    def draw(self, screen):
        """
        Draws the heads-up display
        """
        for i in range(len(self.heart)):
            if self.heart[i] == True:
                screen.blit_rel(self.heart_sprites[0], self.heart_positions[i])
            else:
                screen.blit_rel(self.heart_sprites[1], self.heart_positions[i])
        screen.blit_rel(self.weapon_sprites[self.current_weapon], self.weapon_position)

class Player(Entity):
    """
    Main character class
    """
    def __init__(self):
        super().__init__(np.array([MAP_WIDTH, MAP_HEIGHT])/2, graphics_dict['player'].get_image(0))
        self.health = 5
        self.velocity = 5
        self.hud = Hud(self.health, graphics_dict['items'])
        self.states = []
        for i in range(graphics_dict['player'].get_size()):
            self.states.append(graphics_dict['player'].get_image(i))
        self.weapon = self.states[0]
        self.current_state = self.states[0]

    def set_weapon(self, key):
        """
        Sets a weapon for the player
        """
        if key == K_1:
            self.weapon = self.states[0]
            self.update_sprite(self.states[0])
            self.current_state = self.weapon
        elif key == K_2:
            self.weapon = self.states[1]
            self.update_sprite(self.states[1])
            self.current_state = self.weapon
        elif key == K_3:
            self.weapon = self.states[2]
            self.update_sprite(self.states[2])
            self.current_state = self.weapon

    def update(self, key=None):
        """
        Updates the current player's state and heads-up display.
        """
        if key in [K_1, K_2, K_3]:
            self.set_weapon(key)
        elif key in [K_w, K_a, K_s, K_d]:
            self.current_state = self.states[3]
            self.update_sprite(self.states[3])
        else:
            self.current_state = self.weapon
            self.update_sprite(self.current_state)
        self.hud.update(key)

    def draw(self, screen):
        """
        Draws the player's animation
        """
        super().draw(screen)
        self.hud.draw(screen)
