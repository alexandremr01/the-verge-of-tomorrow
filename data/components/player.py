import pygame

from ..constants import SCREEN_WIDTH, SCREEN_HEIGHT, MAP_WIDTH, MAP_HEIGHT, FRAMES_PER_SECOND
from .base.entity import Entity
from pygame.locals import *
import numpy as np


class Player(Entity):
    """
    Main character class
    """
    def __init__(self, graphics):
        super().__init__(np.array([MAP_WIDTH, MAP_HEIGHT])/2, graphics.get_image(0))
        self.health = 10
        self.velocity = 5
        self.states = []
        for i in range(graphics.get_size()):
            self.states.append(graphics.get_image(i))
        self.weapon = self.states[0]
        self.current_state = self.states[0]
    
    def set_weapon(self, key):
        """
        Sets a weapon for the player
        """
        if key == pygame.K_1:
            self.weapon = self.states[0]
            self.update_sprite(self.states[0])
            self.current_state = self.weapon
        elif key == pygame.K_2:
            self.weapon = self.states[1]
            self.update_sprite(self.states[1])
            self.current_state = self.weapon
        elif key == pygame.K_3:
            self.weapon = self.states[2]
            self.update_sprite(self.states[2])
            self.current_state = self.weapon

    def update(self, key=None):
        """
        Updates the current player's state.
        """
        if key in [pygame.K_1, pygame.K_2, pygame.K_3]:
            self.set_weapon(key)
        elif key in [pygame.K_w, pygame.K_a, pygame.K_s, pygame.K_d]:
            self.current_state = self.states[3]
            self.update_sprite(self.states[3])
        else:
            self.current_state = self.weapon
            self.update_sprite(self.current_state)

    def draw(self, surface, screen_pos):
        """
        Draws the player's animation
        """
        super().draw(surface, screen_pos)



