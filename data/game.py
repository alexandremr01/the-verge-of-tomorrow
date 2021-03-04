"""
Contains game class, central class of application
"""

import pygame

from .constants import SCREEN_WIDTH, SCREEN_HEIGHT, FRAMES_PER_SECOND
from .screens.title import Title
from .screens.base.state_machine import StateMachine

class Game:
    """
    Main class of the game, handles highest level functions
    """
    def __init__(self):
        self.running = True
        self.events = None

        self.window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption('Verge of tomorrow')

        state_dict = {'TITLE'   : Title()}
        self.state_machine = StateMachine(state_dict, 'TITLE')

    def main(self):
        """
        Runs main loop, where state and time is defined
        """
        while self.running:
            pygame.time.Clock().tick(FRAMES_PER_SECOND)

            self.handle_input()
            self.state_machine.update(self.events, self.window)
            pygame.display.update()

    def handle_input(self):
        """
        Function that responds to information given by user through keyboard
        """
        self.events = pygame.event.get()
        for event in self.events:
            if event.type == pygame.QUIT:
                self.running = False
