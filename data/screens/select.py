"""
Screen with multiple options. Player can
go to either about screen or play screen
"""

import pygame

from .base.state import State
from ..utils import is_in_rect
from ..constants import RED, ORANGE, SCREEN_WIDTH, SCREEN_HEIGHT, BASE_SOUNDTRACK_DIR, TITLE_FRAMERATE, BASE_FONT_DIR
from ..setup import sound_dict, graphics_dict

class Select(State):
    """
    Screen where player selects what he wants to do
    """
    def __init__(self):
        super().__init__()

        font = pygame.font.Font(BASE_FONT_DIR + 'ARCADECLASSIC.TTF',
                                28,
                                bold=True)

        self.title_graphics = graphics_dict['title']
        self.time = pygame.time.get_ticks()
        self.last_transition_title_time = 0
        self.counter_title = 0

        self.button_up = graphics_dict['button'].get_image(0, (136, 40))
        self.button_down = graphics_dict['button'].get_image(1, (136, 40))

        self.about_surface = font.render('About', False, RED)
        about_button_center = (SCREEN_WIDTH // 2, 380)
        self.about_button_rect = self.button_up.get_rect(center=about_button_center)
        self.about_rect = self.about_surface.get_rect(center=about_button_center)
        self.about_button = self.button_up

        self.manual_surface = font.render('Manual', False, RED)
        manual_button_center = (SCREEN_WIDTH // 2, 480)
        self.manual_button_rect = self.button_up.get_rect(center=manual_button_center)
        self.manual_rect = self.manual_surface.get_rect(center=manual_button_center)
        self.manual_button = self.button_up

        self.play_surface = font.render('Play', False, RED)
        play_button_center = (SCREEN_WIDTH // 2, 580)
        self.play_button_rect = self.button_up.get_rect(center=play_button_center)
        self.play_rect = self.play_surface.get_rect(center=play_button_center)
        self.play_button = self.button_up

    def update(self):
        self.time = pygame.time.get_ticks()
        if self.time - self.last_transition_title_time >= TITLE_FRAMERATE:
            self.last_transition_title_time = self.time
            self.counter_title += 1
            if self.counter_title > 4:
                self.counter_title = 0
        if (self.about_button is self.button_up 
            and is_in_rect(self.about_button_rect, pygame.mouse.get_pos())):
            self.about_button = self.button_down
            sound_dict['menu_select'].play()
        elif not is_in_rect(self.about_button_rect, pygame.mouse.get_pos()):
            self.about_button = self.button_up
        if (self.manual_button is self.button_up
            and is_in_rect(self.manual_button_rect, pygame.mouse.get_pos())):
            self.manual_button = self.button_down
            sound_dict['menu_select'].play()
        elif not is_in_rect(self.manual_button_rect, pygame.mouse.get_pos()):
            self.manual_button = self.button_up
        if (self.play_button is self.button_up 
            and is_in_rect(self.play_button_rect, pygame.mouse.get_pos())):
            self.play_button = self.button_down
            sound_dict['menu_select'].play()
        elif not is_in_rect(self.play_button_rect, pygame.mouse.get_pos()):
            self.play_button = self.button_up

    def draw(self, screen):
        """
        Draws the options the game provides for the player to select
        """
        screen.blit_rel(self.title_graphics[self.counter_title], (0, 0))
        screen.blit_rel(self.about_button, self.about_button_rect)
        screen.blit_rel(self.manual_button, self.manual_button_rect)
        screen.blit_rel(self.play_button, self.play_button_rect)

        screen.blit_rel(self.about_surface, self.about_rect)
        screen.blit_rel(self.manual_surface, self.manual_rect)
        screen.blit_rel(self.play_surface, self.play_rect)

    def handle_input(self, events, keys):
        """
        If about box is clicked, goes to about screen,
        else if play box is clicked, initiates game
        """
        if pygame.mouse.get_pressed()[0]:
            if is_in_rect(self.about_button_rect, pygame.mouse.get_pos()):
                sound_dict['beep'].play()
                self.next = 'ABOUT'
                self.clear_window = True
            elif is_in_rect(self.manual_button_rect, pygame.mouse.get_pos()):
                sound_dict['beep'].play()
                self.next = 'MANUAL'
                self.clear_window = True   
            elif is_in_rect(self.play_button_rect, pygame.mouse.get_pos()):
                sound_dict['beep'].play()
                self.next = 'PLAY'
                self.clear_window = True
                pygame.mixer.music.stop()
                pygame.mixer.music.unload()
                pygame.mixer.music.load(BASE_SOUNDTRACK_DIR + 'dark_ambiance.wav')
                pygame.mixer.music.play(-1)
