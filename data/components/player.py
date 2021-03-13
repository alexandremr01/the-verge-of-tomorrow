import pygame

from ..constants import SCREEN_WIDTH, SCREEN_HEIGHT, FRAMES_PER_SECOND
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
        self.last_request_time = 0

    def get_position(self):
        """
        Returns the current player's state position
        """
        return self.current_state.get_position()
    
    def set_weapon(self, key):
        """
        Sets a weapon for the player
        """
        if key == pygame.K_1:
            self.weapon = self.states[0]
            self.current_state = self.weapon
        elif key == pygame.K_2:
            self.weapon = self.states[1]
            self.current_state = self.weapon
        elif key == pygame.K_3:
            self.weapon = self.states[2]
            self.current_state = self.weapon

    def update(self, time, key=None, weapon=None):
        """
        Updates the current player's state.
        """
        if key in [pygame.K_1, pygame.K_2, pygame.K_3]:
            self.set_weapon(key)
        elif key in [pygame.K_w, pygame.K_a, pygame.K_s, pygame.K_d]:
            self.current_state = self.states[3]
            self.last_request_time = time

    def draw(self, surface, time):
        """
        Draws the player's animation
        """
        if self.current_state == self.states[3]:
            if time - self.last_request_time > 100.0:
                self.current_state = self.weapon
        self.current_state.draw(surface)
            
