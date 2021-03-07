"""
Main screen, where the game actually occurs
"""

from .base.state import State
from ..test_maps import WaveMap
from ..constants import BLACK

class Play(State):
    """
    Screen of the game where the user needs to
    survive as much as possible
    """
    def __init__(self):
        super().__init__()

        self.map = WaveMap()

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

    def handle_input(self, events):
        pass
