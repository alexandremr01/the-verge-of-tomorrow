"""
Screen with multiple options. Player can
go to either about screen or play screen
"""

import pygame

from .base.state import State
from ..utils import is_in_rect
from ..constants import WHITE, ORANGE, SCREEN_WIDTH, SCREEN_HEIGHT

class Select(State):
    """
    Screen where player selects what he wants to do
    """
    def __init__(self):
        super().__init__()

        font = pygame.font.SysFont('Arial', 25)

        self.about_surface = font.render('About', False, WHITE)
        about_center = (SCREEN_WIDTH/3, SCREEN_HEIGHT/3)
        self.about_rect = self.about_surface.get_rect(center=about_center)

        self.play_surface = font.render('Play', False, WHITE)
        play_center = (SCREEN_WIDTH/3, 2*SCREEN_HEIGHT/3)
        self.play_rect = self.play_surface.get_rect(center=play_center)

    def update(self):
        pass

    def draw(self, screen):
        """
        Draws the options the game provides for the player to select
        """
        pygame.draw.rect(screen, ORANGE, self.about_rect)
        screen.blit_rel(self.about_surface, self.about_rect)

        pygame.draw.rect(screen, ORANGE, self.play_rect)
        screen.blit_rel(self.play_surface, self.play_rect)

    def handle_input(self, events, keys):
        """
        If about box is clicked, goes to about screen,
        else if play box is clicked, initiates game
        """
        if pygame.mouse.get_pressed()[0]:
            if is_in_rect(self.about_rect, pygame.mouse.get_pos()):
                self.next = 'ABOUT'
                self.clear_window = True
            elif is_in_rect(self.play_rect, pygame.mouse.get_pos()):
                self.next = 'PLAY'
                self.clear_window = True
