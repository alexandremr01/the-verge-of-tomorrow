"""
Manual screen that shows game's instructions
"""

import pygame

from .base.state import State
from ..utils import is_in_rect
from ..constants import WHITE, BUTTON_RED, BLACK, SCREEN_HEIGHT, SCREEN_WIDTH, BASE_FONT_DIR
from ..constants import MANUAL_SCREEN_INPUT_LAG
from ..setup import graphics_dict, sound_dict


class ManualPage():
    """
    The base class of a manual page with instructions
    """
    def __init__(self):
        self.text_font = pygame.font.Font(BASE_FONT_DIR + 'ARCADECLASSIC.TTF', 20)
        self.page_title_font = pygame.font.Font(BASE_FONT_DIR + 'ARCADECLASSIC.TTF', 40)
    
    def draw(self, screen):
        """
        Draws the page on the screen
        """
        pass

class Keys(ManualPage):
    """
    Contains instructions about game's keys
    """
    def __init__(self):
        super().__init__()
        
        self.keys_surface = self.page_title_font.render('Keys', False, BLACK)
        keys_center = (400, 100)
        self.keys_rect = self.keys_surface.get_rect(center=keys_center)

    def draw(self, screen):
        """
        Draws the keys' instructions on the screen
        """
        screen.blit_rel(self.keys_surface, self.keys_rect)


class Items(ManualPage):
    """
    Contains instructions about items
    """
    def __init__(self):
        super().__init__()

        self.items_surface = self.page_title_font.render('Items', False, BLACK)
        items_center = (400, 100)
        self.items_rect = self.items_surface.get_rect(center=items_center)
    
    def draw(self, screen):
        """
        Draws items' informations 
        """
        screen.blit_rel(self.items_surface, self.items_rect)

class Manual(State):
    """
    Collection of manual's pages with game's instructions
    """
    def __init__(self):
        super().__init__()
        font = pygame.font.Font(BASE_FONT_DIR + 'ARCADECLASSIC.TTF', 28)

        self.background_surface = graphics_dict['about']
        self.background_rect = self.background_surface.get_rect(center=(SCREEN_WIDTH//2, 
                                                                        SCREEN_HEIGHT//2))

        self.button_up = graphics_dict['button'].get_image(0, (136, 40))
        self.button_down = graphics_dict['button'].get_image(1, (136, 40))
        
        self.next_surface = font.render('NEXT', False, BUTTON_RED)
        next_button_center = (680, 35)
        self.next_button_rect = self.button_up.get_rect(center=next_button_center)
        self.next_rect = self.next_surface.get_rect(center=next_button_center)
        self.next_button = self.button_up

        self.back_surface = font.render('BACK', False, BUTTON_RED)
        back_button_center = (100, 35)
        self.back_button_rect = self.button_up.get_rect(center=back_button_center)
        self.back_rect = self.back_surface.get_rect(center=back_button_center)
        self.back_button = self.button_up

        self.manual_screens = [Keys(), Items()] # contains text and images to display
        self.current_manual_page = 0

        self.last_input_time = 0

    def update(self):
        """
        Updates buttons' state according to mouse position
        """
        mouse_pos = pygame.mouse.get_pos()
        if self.current_manual_page is not len(self.manual_screens) - 1:
            if (self.next_button is self.button_up and is_in_rect(self.next_button_rect, mouse_pos)):
                self.next_button = self.button_down
                sound_dict['menu_select'].play()
            elif not is_in_rect(self.next_button_rect, mouse_pos):
                self.next_button = self.button_up        
        if (self.back_button is self.button_up and is_in_rect(self.back_button_rect, mouse_pos)):
            self.back_button = self.button_down
            sound_dict['menu_select'].play()
        elif not is_in_rect(self.back_button_rect, mouse_pos):
            self.back_button = self.button_up
        
    def draw(self, screen):
        """
        Draws the current manual page on the screen
        """
        screen.blit_rel(self.background_surface, self.background_rect)

        if self.current_manual_page is not len(self.manual_screens) - 1:
            screen.blit_rel(self.next_button, self.next_button_rect)
            screen.blit_rel(self.next_surface, self.next_rect)
        
        screen.blit_rel(self.back_button, self.back_button_rect)
        screen.blit_rel(self.back_surface, self.back_rect)
        
        self.manual_screens[self.current_manual_page].draw(screen)

    def handle_input(self, events, keys):
        """
        If the back button is pressed, it returns to select screen
        """
        time = pygame.time.get_ticks()
        if pygame.mouse.get_pressed()[0] and time - self.last_input_time >= MANUAL_SCREEN_INPUT_LAG:
            self.last_input_time = time
            if (is_in_rect(self.back_button_rect, 
                          pygame.mouse.get_pos()) and self.current_manual_page == 0):
                sound_dict['beep'].play()          
                self.next = 'SELECT'
                self.clear_window = True
            elif (is_in_rect(self.next_button_rect, pygame.mouse.get_pos()) and 
                  self.current_manual_page is not len(self.manual_screens) - 1):
                sound_dict['beep'].play()
                self.current_manual_page += 1
            elif is_in_rect(self.back_button_rect, pygame.mouse.get_pos()):
                if self.current_manual_page is not 0:
                    sound_dict['beep'].play()
                    self.current_manual_page -= 1
