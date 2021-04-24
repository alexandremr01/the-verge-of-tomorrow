"""
Manual screen that shows game's instructions
"""

import pygame

from .base.state import State
from ..utils import is_in_rect
from ..constants import WHITE, ORANGE, RED, BLACK, SCREEN_HEIGHT, SCREEN_WIDTH, BASE_FONT_DIR
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
        #screen.blit_rel(self.keys_surface, self.keys_rect)

        y = 80

        name_font = pygame.font.Font(BASE_FONT_DIR + 'ARCADECLASSIC.TTF', 60)
        x = name_font.render('OBJECTIVE', True, BLACK)
        screen.blit_rel(x, ((800 - x.get_width())/2 , y))
        
        y+=80

        name_font = pygame.font.Font(BASE_FONT_DIR + 'ARCADECLASSIC.TTF', 30)
        objectiveText = ['The   goal   of   the   game   is   to   survive',
                         'as   long   as   possible   running    away',
                        'from   the    enemies   or    killing    them']
        for phrase in objectiveText:
            x = name_font.render(phrase, True, BLACK)
            screen.blit_rel(x, ((800 - x.get_width())/2 , y))
            y+=25
        
        y+=30

        name_font = pygame.font.Font(BASE_FONT_DIR + 'ARCADECLASSIC.TTF', 60)
        x = name_font.render('KEYS', True, BLACK)
        screen.blit_rel(x, ((800 - x.get_width())/2 , y))

        y+=80

        name_font = pygame.font.Font(BASE_FONT_DIR + 'ARCADECLASSIC.TTF', 30)
        keysText = ['W    to    move    UP',
                    'S    to    move    DOWN',
                    'A    to    move    LEFT',
                    'D    to    move   RIGHT',
                    'Hold   SHIFT    to   RUN',
                    'LEFT   BUTTON   to   SHOOT',
                    '1   2   3   to   switch   weapon',
                    'Q  to   use   item   in   bag']
        for phrase in keysText:
            x = name_font.render(phrase, True, BLACK)
            screen.blit_rel(x, ((800 - x.get_width())/2 , y))
            y+=48
        y+=15



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
        #screen.blit_rel(self.items_surface, self.items_rect)

        y = 80
        screen.blit_rel(graphics_dict['items'].get_image(2), (400,155))
        screen.blit_rel(graphics_dict['items'].get_image(0), (425,265))
        screen.blit_rel(graphics_dict['items'].get_image(1), (450,375))
        screen.blit_rel(graphics_dict['items'].get_image(10), (280,485))
        screen.blit_rel(graphics_dict['items'].get_image(3), (280,595))


        name_font = pygame.font.Font(BASE_FONT_DIR + 'ARCADECLASSIC.TTF', 60)
        x = name_font.render('Items', True, BLACK)
        screen.blit_rel(x, ((800 - x.get_width())/2 , y))
        
        y+=70

        name_font = pygame.font.Font(BASE_FONT_DIR + 'ARCADECLASSIC.TTF', 35)
        item_font = pygame.font.Font(BASE_FONT_DIR + 'ARCADECLASSIC.TTF', 45)

        listItems = ['Red   Potion', 'Blue   Potion', 'Green   Potion', 'Chest', 'Skull']
        descriptionItems = ['restores   one   heart',
                            'removes   bleeding   status',
                            'removes   slow   status',
                            'gives   ammo   to   a   random   gun',
                            'gives   the   strong   status']

        i = 0
        for phrase in descriptionItems:
            z = item_font.render(listItems[i], True, BLACK)
            screen.blit_rel(z, (150 , y))
            y+= 50
            
            x = name_font.render(phrase, True, BLACK)
            screen.blit_rel(x, (170 , y))
            y+=60

            i+= 1


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
        
        self.next_surface = font.render('NEXT', False, RED)
        next_button_center = (680, 35)
        self.next_button_rect = self.button_up.get_rect(center=next_button_center)
        self.next_rect = self.next_surface.get_rect(center=next_button_center)
        self.next_button = self.button_up

        self.back_surface = font.render('BACK', False, RED)
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
