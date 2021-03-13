import pygame

from ..constants import SCREEN_WIDTH, SCREEN_HEIGHT
from .base.entity import Entity

class Player():
    """
    Main character class
    """
    def __init__(self, graphics):
        self.states = []
        for i in range(graphics.get_size()):
            self.states.append(Entity((SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2), graphics.get_image(i)))
        self.weapon = self.states[0]
        self.current_state = self.states[0]

    def get_position(self):
        """
        Returns the current player's state position
        """
        return self.weapon.get_position()
    
    def set_weapon(self, weapon):
        """
        Sets a weapon for the player
        """
        if weapon == 'submachine':
            self.weapon = self.states[0]
        elif weapon == 'rifle':
            self.weapon = self.states[1]
        elif weapon == 'shotgun':
            self.weapon = self.states[2]
 
    def update(self, key=None, weapon=None):
        """
        Updates the current player's state.
        """
        self.set_weapon(weapon)
        if key in [pygame.K_w, pygame.K_a, pygame.K_s, pygame.K_d]:
            self.current_state = self.states[3]
        else:
            self.current_state = self.weapon

    def draw(self, surface):
        """
        Draws the player
        """
        self.current_state.draw(surface)
