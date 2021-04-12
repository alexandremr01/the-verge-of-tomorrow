"""
About screen, with text about the developers
creators of this game
"""

import pygame

from .base.state import State
from ..utils import is_in_rect
from ..constants import WHITE, BLACK, BUTTON_RED, SCREEN_HEIGHT, SCREEN_WIDTH, BASE_FONT_DIR
from ..setup import graphics_dict, sound_dict

class About(State):
    """
    Exposition screen with text about the developers
    """
    def __init__(self):
        super().__init__()
        font = pygame.font.Font(BASE_FONT_DIR + 'ARCADECLASSIC.TTF', 28)

        self.menu_about_graphics = graphics_dict['about']

        self.button_up = graphics_dict['button'].get_image(0, (136, 40))
        self.button_down = graphics_dict['button'].get_image(1, (136, 40))

        self.back_surface = font.render('BACK', False, BUTTON_RED)
        back_button_center = (100, 35)
        self.back_button_rect = self.button_up.get_rect(center=back_button_center)
        self.back_rect = self.back_surface.get_rect(center=back_button_center)
        self.back_button = self.button_up

    def update(self):
        """
        Updates back button's state
        """
        mouse_pos = pygame.mouse.get_pos()
        if (self.back_button is self.button_up and is_in_rect(self.back_button_rect, mouse_pos)):
            self.back_button = self.button_down
            sound_dict['menu_select'].play()
        elif not is_in_rect(self.back_button_rect, mouse_pos):
            self.back_button = self.button_up

    def draw(self, screen):
        """
        Draws the about text
        """
        screen.blit_rel(self.menu_about_graphics, (0, 0))
        
        font_30 = pygame.font.Font(BASE_FONT_DIR + 'ARCADECLASSIC.TTF', 30)
        font_40 = pygame.font.Font(BASE_FONT_DIR + 'ARCADECLASSIC.TTF', 40)
        font_60 = pygame.font.Font(BASE_FONT_DIR + 'ARCADECLASSIC.TTF', 60)

        paragraph_1 = ['This   game   was   a   assigment   for',
                       'CES 22   course   at   ITA']

        names = ['Alexandre   Maranhao',
                 'Alvaro   Tedeschi',
                 'Davi   Vasconcelos',
                 'Gabriel   Rodrigues',
                 'Kenji   Yamane']
        
        screen_y = 100
        for phrase in paragraph_1:
            phrase_surface = font_30.render(phrase, True, BLACK)
            screen.blit_rel(phrase_surface, ((800 - phrase_surface.get_width())/2, screen_y))
            screen_y += 25
        
        screen_y += 40
        team_surface = font_60.render('TEAM', True, BLACK)
        screen.blit_rel(team_surface, ((800 - team_surface.get_width())/2 , screen_y))
        screen_y += 80

        for name in names:
            name_surface = font_40.render(name, True, BLACK)
            screen.blit_rel(name_surface, ((800 - name_surface.get_width())/2 , screen_y))
            screen_y += 35

        screen.blit_rel(self.back_button, self.back_button_rect)
        screen.blit_rel(self.back_surface, self.back_rect)    

    def handle_input(self, events, keys):
        """
        If the back button is pressed, it returns to select screen
        """
        if pygame.mouse.get_pressed()[0]:
            if is_in_rect(self.back_button_rect, pygame.mouse.get_pos()):
                sound_dict['beep'].play()
                self.next = 'SELECT'
                self.clear_window = True
