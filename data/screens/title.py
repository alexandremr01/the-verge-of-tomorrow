"""
Title screen. Just for exposure
"""

import pygame

from .base.state import State
from ..constants import WHITE, SCREEN_WIDTH, SCREEN_HEIGHT
from ..setup import sound_dict

class Title(State):
    """
    Screen that shows game title. Goes to select
    if any key is pressed
    """
    def __init__(self):
        super().__init__()

        title_font = pygame.font.SysFont('Arial', 30)
        self.title_surface = title_font.render('Verge of Tomorrow', False, WHITE)
        title_center = (SCREEN_WIDTH/2, SCREEN_HEIGHT/2)
        self.title_rect = self.title_surface.get_rect(center=title_center)

        helper_font = pygame.font.SysFont('Arial', 20)
        self.helper_surface = helper_font.render('Press any key to continue', False, WHITE)
        helper_center = (SCREEN_WIDTH/2, SCREEN_HEIGHT/2 + SCREEN_WIDTH/3)
        self.helper_rect = self.helper_surface.get_rect(center=helper_center)

    def update(self):
        pass

    def draw(self, screen):
        """
        Draws title of the game and helper text
        """
        screen.blit_rel(self.title_surface, self.title_rect)
        screen.blit_rel(self.helper_surface, self.helper_rect)

    def handle_input(self, events, keys):
        """
        On any key press, sets next state to be select
        """
        for event in events:
            if event.type == pygame.KEYDOWN:
                self.next = 'SELECT'
                self.clear_window = True
                sound_dict['beep'].play()
