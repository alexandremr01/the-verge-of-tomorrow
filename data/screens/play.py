"""
Main screen, where the game actually occurs
"""

from .base.state import State
from ..components.base.sprite import SpriteSheet
from ..map import RandomMap

class Play(State):
    """
    Screen of the game where the user needs to
    survive as much as possible
    """
    def __init__(self):
        super().__init__()

        sprite_sheet_loc = '../survival-game/resources/graphics/spritesheet-example.png'
        self.spritesheet = SpriteSheet(sprite_sheet_loc, 16, 128, 160)
        self.map = RandomMap(self.spritesheet)

    def update(self):
        pass

    def draw(self, surface):
        """
        Draws the game
        """
        self.map.draw(surface)

    def handle_input(self, events):
        pass
