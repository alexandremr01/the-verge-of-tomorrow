"""
Main screen, where the game actually occurs
"""

import pygame

from .base.state import State
from ..components.player import Player
from ..map import Map
from ..test_maps import WaveMap
from ..constants import BLACK, FRAMES_PER_SECOND


class Play(State):
    """
    Screen of the game where the user needs to
    survive as much as possible
    """
    def __init__(self, graphics):
        super().__init__()
        self.map = Map(graphics)
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

    def handle_input(self, events, keys):
        """
        Responds to inputs given through keyboard
        """
        self.map.handle_input(events)

