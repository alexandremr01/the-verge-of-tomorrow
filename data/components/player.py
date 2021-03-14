import pygame
import numpy as np

from ..constants import SCREEN_WIDTH, SCREEN_HEIGHT, MAP_WIDTH, MAP_HEIGHT, FRAMES_PER_SECOND
from .base.entity import Entity
from .base.sprite import Sprite
from pygame.locals import *


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

    def draw(self, surface):
        """
        Draws the heads-up display
        """
        for i in range(len(self.heart)):
            if self.heart[i] == True:
                surface.blit(self.heart_sprites[0], self.heart_positions[i])
            else:
                surface.blit(self.heart_sprites[1], self.heart_positions[i])
        surface.blit(self.weapon_sprites[self.current_weapon], self.weapon_position)

class Player(Entity):
    """
    Main character class
    """
    def __init__(self, graphics):
        """
        param graphics : collection of all game's graphics
        type graphics : dict of SpriteSheet
        """
        super().__init__(np.array([MAP_WIDTH, MAP_HEIGHT])/2, graphics['player'].get_image(0))
        self.health = 5
        self.velocity = 5
        self.hud = Hud(self.health, graphics['items'])
        self.states = []
        for i in range(graphics['player'].get_size()):
            self.states.append(graphics['player'].get_image(i))
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

    def draw(self, surface, screen_pos):
        """
        Draws the player's animation
        """
        super().draw(surface, screen_pos)
        self.hud.draw(surface)