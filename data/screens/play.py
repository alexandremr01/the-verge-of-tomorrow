"""
Main screen, where the game actually occurs
"""

from .base.state import State
from data.map.map import Map
from ..constants import BLACK, TRANSITION_BETWEEN_SCREENS


class Play(State):
    """
    Screen of the game where the user needs to
    survive as much as possible
    """
    def __init__(self):
        super().__init__()
        self.map = Map()
        self.delay_to_game_over = 0

    def update(self):
        """
        Updates the game
        """
        self.map.update()

        if not self.map.player.is_alive():
            self.delay_to_game_over += 1
        if self.delay_to_game_over == TRANSITION_BETWEEN_SCREENS:
            self.next = 'OVER'
            self.clear_window = True

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
