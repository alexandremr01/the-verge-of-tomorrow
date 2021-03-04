"""
About screen, with text about the developers
creators of this game
"""

import pygame

from .base.state import State
from ..utils import is_in_rect
from ..constants import WHITE, ORANGE, SCREEN_HEIGHT, SCREEN_WIDTH

class About(State):
    """
    Exposition screen with text about the developers
    """
    def __init__(self):
        super().__init__()
        font = pygame.font.SysFont('Arial', 30)

        self.about_surface = font.render('About', False, WHITE)
        about_center = (SCREEN_WIDTH/2, SCREEN_HEIGHT/2)
        self.about_rect = self.about_surface.get_rect(center=about_center)

        self.back_surface = font.render('Back to select', False, WHITE)

    def update(self):
        pass

    def draw(self, surface):
        """
        Draws the about text
        """
        surface.blit(self.about_surface, self.about_rect)

        pygame.draw.rect(surface, ORANGE, self.back_surface.get_rect())
        surface.blit(self.back_surface, self.back_surface.get_rect())

    def handle_input(self, events):
        """
        If the back button is pressed, it returns to select screen
        """
        if pygame.mouse.get_pressed()[0]:
            if is_in_rect(self.back_surface.get_rect(), pygame.mouse.get_pos()):
                self.next = 'SELECT'
                self.clear_window = True
