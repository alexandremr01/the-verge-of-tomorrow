"""
Contains game class, central class of application
"""

import pygame

from .constants import SCREEN_WIDTH, SCREEN_HEIGHT, FRAMES_PER_SECOND
from .screens.title import Title
from .screens.select import Select
from .screens.play import Play
from .screens.about import About
from .screens.over import Over
from .screens.base.state_machine import StateMachine
from .screens.base.screen_surface import ScreenSurface
from .setup import load_graphics, load_sound, load_music

class Game:
    """
    Main class of the game, handles highest level functions
    """
    def __init__(self):
        self.running = True
        self.events = None
        self.keys = None

        self.clock = pygame.time.Clock()
        self.window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.screen = ScreenSurface(self.window.get_rect())
        pygame.display.set_caption('The Verge of Tomorrow')
        load_graphics()
        load_sound()
        load_music()

        state_dict = {
            'TITLE': Title(),
            'SELECT': Select(),
            'PLAY': Play(),
            'ABOUT': About(),
            'OVER': Over()
        }
        self.state_machine = StateMachine(state_dict, 'TITLE')

    def main(self):
        """
        Runs main loop, where state and time is defined
        """
        while self.running:
            self.clock.tick(FRAMES_PER_SECOND)

            self.handle_input()
            self.keys = pygame.key.get_pressed()
            self.state_machine.update(self.events, self.keys, self.screen)

            self.window.blit(self.screen, (0, 0))
            pygame.display.update()

    def handle_input(self):
        """
        Function that responds to information given by user through keyboard
        """
        self.events = pygame.event.get()
        for event in self.events:
            if event.type == pygame.QUIT:
                self.running = False
