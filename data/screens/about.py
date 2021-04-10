"""
About screen, with text about the developers
creators of this game
"""

import pygame

from .base.state import State
from ..utils import is_in_rect
from ..constants import WHITE, ORANGE, BLACK, SCREEN_HEIGHT, SCREEN_WIDTH, BASE_FONT_DIR
from ..setup import graphics_dict

class About(State):
    """
    Exposition screen with text about the developers
    """
    def __init__(self):
        super().__init__()
        font = pygame.font.SysFont('Arial', 30)

        self.menu_about_graphics = graphics_dict['about']

        self.about_surface = font.render('About', False, WHITE)
        about_center = (SCREEN_WIDTH/2, SCREEN_HEIGHT/2)
        self.about_rect = self.about_surface.get_rect(center=about_center)

        self.back_surface = font.render('Back to select', False, WHITE)

    def update(self):
        pass

    def draw(self, screen):
        """
        Draws the about text
        """
        #screen.blit_rel(self.about_surface, self.about_rect)
        screen.blit_rel(self.menu_about_graphics, (0, 0))
        
        y = 100
        name_font = pygame.font.Font(BASE_FONT_DIR + 'ARCADECLASSIC.TTF', 30)
        paragraph1 = ['This   game   was   a   assigment   for',
                      'CES 22   course   at   ITA']
        for phrase in paragraph1:
            x = name_font.render(phrase, True, BLACK)
            screen.blit_rel(x, ((800 - x.get_width())/2 , y))
            y+=25
        
        y+=40
        name_font = pygame.font.Font(BASE_FONT_DIR + 'ARCADECLASSIC.TTF', 60)
        x = name_font.render('TEAM', True, BLACK)
        screen.blit_rel(x, ((800 - x.get_width())/2 , y))
        y+=80

        name_font = pygame.font.Font(BASE_FONT_DIR + 'ARCADECLASSIC.TTF', 40)
        names = ['Alexandre   Maranhao',
                'Alvaro   Tedeschi',
                'Davi   Vasconcelos',
                'Gabriel   Rodrigues',
                'Kenji   Yamane']
        for name in names:
            x = name_font.render(name, True, BLACK)
            screen.blit_rel(x, ((800 - x.get_width())/2 , y))
            y+=35

        pygame.draw.rect(screen, ORANGE, self.back_surface.get_rect())
        screen.blit_rel(self.back_surface, self.back_surface.get_rect())

    def handle_input(self, events, keys):
        """
        If the back button is pressed, it returns to select screen
        """
        if pygame.mouse.get_pressed()[0]:
            if is_in_rect(self.back_surface.get_rect(), pygame.mouse.get_pos()):
                self.next = 'SELECT'
                self.clear_window = True
