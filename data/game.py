"""
Contains game class
"""

import pygame

from .constants import SCREEN_WIDTH, SCREEN_HEIGHT, FRAMES_PER_SECOND, BLACK

class Game:
    """
    Main class of the game, handles highest level functions
    """
    def __init__(self):
        self.running = True
        self.window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

        pygame.display.set_caption('Verge of tomorrow')

    def main(self):
        """
        Runs main loop, where state and time is defined
        """
        while self.running:
            pygame.time.Clock().tick(FRAMES_PER_SECOND)
            self.handle_input()

            self.window.fill(BLACK)
            pygame.display.update()

    def handle_input(self):
        """
        Function that responds to information given by user through keyboard
        """

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
