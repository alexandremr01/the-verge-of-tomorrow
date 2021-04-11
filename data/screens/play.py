"""
Main screen, where the game actually occurs
"""

import pygame

from .base.state import State
from data.map.map import Map
from ..constants import BLACK, TRANSITION_BETWEEN_SCREENS


class Play(State):
    """
    Screen of the game where the user needs to
    survive as much as possible
    """
    def __init__(self):
        super().__init__()
        self.map = Map()
        self.delay_to_game_over = 0

    def update(self):
        """
        Updates the game
        """
        self.map.update()

        if not self.map.get_player().is_alive():
            self.delay_to_game_over += 1
        if self.delay_to_game_over == TRANSITION_BETWEEN_SCREENS:
            self.custom_value = self.map.get_player().get_score()
            self.next = 'OVER'
            self.clear_window = True
            pygame.mixer.music.stop()
            pygame.mixer.music.unload()

    def draw(self, screen):
        """
        Draws the game
        """
        screen.fill(BLACK)
        self.map.draw(screen)

    def handle_input(self, events, keys):
        """
        Responds to inputs given through keyboard
        """
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.next = 'PAUSE'

        self.map.handle_input(events)

    def reset(self):
        """
        Resets all variables to start a new game
        """
        self.__init__()
