"""
Title screen. Just for exposure
"""

import pygame

from .base.state import State
from ..constants import WHITE, SCREEN_WIDTH, SCREEN_HEIGHT, TITLE_FRAMERATE, TITLE_MESSAGE_FRAMERATE
from ..setup import sound_dict, graphics_dict, music_dict

class Title(State):
    """
    Screen that shows game title. Goes to select
    if any key is pressed
    """
    def __init__(self):
        super().__init__()

        self.title_graphics = graphics_dict['title']
        self.time = pygame.time.get_ticks()
        self.last_transition_title_time = 0
        self.last_transition_message_time = 0
        self.counter_title = 0
        self.show_message = True

        helper_font = pygame.font.Font('../survival-game/resources/fonts/ARCADECLASSIC.TTF', 20)
        self.helper_surface = helper_font.render('Press   any   key   to   continue', False, WHITE)
        helper_center = (SCREEN_WIDTH/2, SCREEN_HEIGHT/2 + SCREEN_WIDTH/3)
        self.helper_rect = self.helper_surface.get_rect(center=helper_center)

        pygame.mixer.music.play(-1)

    def update(self):
        """
        Updates the current image on the screen
        """
        self.time = pygame.time.get_ticks()
        if self.time - self.last_transition_title_time >= TITLE_FRAMERATE:
            self.last_transition_title_time = self.time
            self.counter_title += 1
            if self.counter_title > 4:
                self.counter_title = 0
        if self.time - self.last_transition_message_time >= TITLE_MESSAGE_FRAMERATE:
            self.last_transition_message_time = self.time
            if self.show_message:
                self.show_message = False
            else:
                self.show_message = True

    def draw(self, screen):
        """
        Draws title of the game and helper text
        """
        screen.blit_rel(self.title_graphics[self.counter_title], (0, 0))
        if self.show_message:
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
