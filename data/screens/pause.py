"""
Screen of pause, pauses the game
when the pause button is pressed
"""

import pygame

from .base.state import State
from ..constants import GRAY_PAUSE_INTENSITY, SCREEN_WIDTH, SCREEN_HEIGHT
from ..constants import BLACK, WHITE, BASE_FONT_DIR

class Pause(State):
    """
    State only accessible by the Play state.
    Freezes play.
    """
    def __init__(self):
        super().__init__()
        self.grayed = False

        helper_font = pygame.font.Font(BASE_FONT_DIR + 'ARCADECLASSIC.TTF', 20)
        self.helper_surface = helper_font.render('Press space to resume', False, WHITE)
        helper_center = (SCREEN_WIDTH/2, 2*SCREEN_HEIGHT/3)
        self.helper_rect = self.helper_surface.get_rect(center=helper_center)

        paused_font = pygame.font.Font(BASE_FONT_DIR + 'ARCADECLASSIC.TTF', 50)
        self.paused_surface = paused_font.render('PAUSED', False, WHITE)
        paused_center = (SCREEN_WIDTH/2, SCREEN_HEIGHT/3)
        self.paused_rect = self.paused_surface.get_rect(center=paused_center)

    def draw(self, screen):
        """
        Draws the game
        """
        if not self.grayed:
            fade = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            fade.fill(BLACK)
            fade.set_alpha(GRAY_PAUSE_INTENSITY)
            screen.blit_rel(fade, (0, 0))

            self.grayed = True

        screen.blit_rel(self.helper_surface, self.helper_rect)
        screen.blit_rel(self.paused_surface, self.paused_rect)

    def handle_input(self, events, keys):
        """
        Responds to inputs given through keyboard
        """
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.grayed = False
                    self.next = 'PLAY'
