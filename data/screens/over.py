"""
Game over screen, which is showed when the player
dies
"""

import pygame

from .base.state import State
from ..constants import WHITE
from ..constants import SCREEN_HEIGHT, SCREEN_WIDTH

class Over(State):
    """
    Screen showed when the player dies
    """
    def __init__(self):
        super().__init__()
        font = pygame.font.SysFont('Arial', 30)

        self.over_surface = font.render('Game Over', False, WHITE)
        over_center = (SCREEN_WIDTH/2, SCREEN_HEIGHT/2)
        self.over_rect = self.over_surface.get_rect(center=over_center)

    def update(self):
        pass

    def draw(self, screen):
        """
        Draws 'game over'
        """
        screen.blit_rel(self.over_surface, self.over_rect)

    def handle_input(self, events, keys):
        """
        If the back button is pressed, it returns to select screen
        """
