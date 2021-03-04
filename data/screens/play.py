"""
Main screen, where the game actually occurs
"""

import pygame

from .base.state import State
from ..constants import WHITE

class Play(State):
    """
    Screen of the game where the user needs to
    survive as much as possible
    """
    def __init__(self):
        super().__init__()

        font = pygame.font.SysFont('Arial', 25)
        self.play_text = font.render('Play', False, WHITE)

    def update(self):
        pass

    def draw(self, surface):
        """
        Draws the game
        """
        surface.blit(self.play_text, (0, 0))

    def handle_input(self, events):
        pass
