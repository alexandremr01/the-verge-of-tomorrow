"""
Main screen, where the game actually occurs
"""

from .base.state import State
from data.map.map import Map
from ..constants import BLACK


class Play(State):
    """
    Screen of the game where the user needs to
    survive as much as possible
    """
    def __init__(self):
        super().__init__()
        self.map = Map()

    def update(self):
        """
        Updates the game
        """
        self.map.update()

    def draw(self, screen):
        """
        Draws the game
        """
        screen.fill(BLACK)
        self.map.draw(screen)

    def handle_input(self, events, keys):
        """
        Responds to inputs given through keyboard
        """
        self.map.handle_input(events)
