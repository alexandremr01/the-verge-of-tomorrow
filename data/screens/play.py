"""
Main screen, where the game actually occurs
"""

import pygame

from .base.state import State
from ..components.player import Player
from ..test_maps import WaveMap
from ..constants import BLACK, FRAMES_PER_SECOND

class Play(State):
    """
    Screen of the game where the user needs to
    survive as much as possible
    """
    def __init__(self, graphics):
        super().__init__()

        self.map = WaveMap()
        self.player = Player(graphics['player'])
        self.time = pygame.time.get_ticks()
        
    def update(self):
        """
        Updates the game
        """
        self.map.update()
        self.time = pygame.time.get_ticks()

    def draw(self, surface):
        """
        Draws the game
        """
        surface.fill(BLACK)
        self.map.draw(surface)
        self.player.draw(surface, self.time)

    def handle_input(self, events, keys):
        """
        Responds to inputs given through keyboard
        """
        if keys[pygame.K_w]:
            self.player.update(self.time, pygame.K_w)
        if keys[pygame.K_a]:
            self.player.update(self.time, pygame.K_a)
        if keys[pygame.K_s]:
            self.player.update(self.time, pygame.K_s)
        if keys[pygame.K_d]:
            self.player.update(self.time, pygame.K_d)
        if keys[pygame.K_1]:
            self.player.update(self.time, pygame.K_1)
        if keys[pygame.K_2]:
            self.player.update(self.time, pygame.K_2)
        if keys[pygame.K_3]:
            self.player.update(self.time, pygame.K_3)