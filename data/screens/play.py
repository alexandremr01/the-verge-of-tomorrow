"""
Main screen, where the game actually occurs
"""

import pygame

from .base.state import State
from ..components.player import Player
from ..test_maps import WaveMap
from ..constants import BLACK

class Play(State):
    """
    Screen of the game where the user needs to
    survive as much as possible
    """
    def __init__(self, graphics):
        super().__init__()

        self.map = WaveMap()
        self.player = Player(graphics['player'])

    def update(self):
        """
        Updates the game
        """
        self.map.update()

    def draw(self, surface):
        """
        Draws the game
        """
        surface.fill(BLACK)
        self.map.draw(surface)
        self.player.draw(surface)

    def handle_input(self, events):
        """
        Responds to inputs given through keyboard
        """
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    self.player.update(pygame.K_w)