"""
Game over screen, which is showed when the player
dies
"""

import pygame

from .base.state import State
from ..constants import RED, WHITE
from ..constants import SCREEN_HEIGHT, SCREEN_WIDTH
from ..setup import sound_dict

class Over(State):
    """
    Screen showed when the player dies
    """
    def __init__(self):
        super().__init__()
        font_large = pygame.font.Font('./resources/fonts/ARCADECLASSIC.TTF', 50)
        font_small = pygame.font.Font('./resources/fonts/ARCADECLASSIC.TTF', 30)

        self.over_surface = font_large.render('Game  Over', False, RED)
        over_center = (SCREEN_WIDTH/2, SCREEN_HEIGHT/2 - 100)
        self.over_rect = self.over_surface.get_rect(center=over_center)
        
        self.message_surface = font_small.render('Press  any  key  to' +  
                                                 '  return  to  menu', False, WHITE)
        message_center = (SCREEN_WIDTH/2, SCREEN_HEIGHT/2 + 200)
        self.message_rect = self.message_surface.get_rect(center=message_center)

    def set_score(self, score):
        """
        Sets player's final score on the screen
        """
        font = pygame.font.Font('./resources/fonts/ARCADECLASSIC.TTF', 40)
        self.score_surface = font.render('SCORE    ' + str(score), False, WHITE)
        self.score_rect = self.score_surface.get_rect(center=(SCREEN_WIDTH/2,
                                                              SCREEN_HEIGHT/2 + 50))
        sound_dict['gameover'].play()

    def draw(self, screen):
        """
        Draws 'game over', player's score, and a instruction message
        """
        screen.blit_rel(self.over_surface, self.over_rect)
        screen.blit_rel(self.message_surface, self.message_rect)
        screen.blit_rel(self.score_surface, self.score_rect)

    def handle_input(self, events, keys):
        """
        If the back button is pressed, it returns to select screen
        """
        for event in events:
            if event.type == pygame.KEYDOWN:
                self.next = 'SELECT'
                self.clear_window = True