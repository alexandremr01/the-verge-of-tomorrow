"""
Main screen, where the game actually occurs
"""

from .base.state import State
from ..map import RandomMap
from ..setup import graphics_dict

class Play(State):
    """
    Screen of the game where the user needs to
    survive as much as possible
    """
    def __init__(self):
        super().__init__()

        self.map = RandomMap(graphics_dict["test_spritesheet"])

    def update(self):
        pass

    def draw(self, surface):
        """
        Draws the game
        """
        self.map.draw(surface)

    def handle_input(self, events):
        pass
