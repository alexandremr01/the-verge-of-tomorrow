"""
Main screen, where the game actually occurs
"""

import pygame

from data.map.map import Map
from .base.state import State
from ..constants import BLACK, PLAY_TO_OVER_DELAY, LOADING_TIME, TITLE_FRAMERATE
from ..constants import WHITE, LOADBAR_HEIGHT, LOADBAR_WIDTH, SCREEN_WIDTH, SCREEN_HEIGHT
from ..setup import graphics_dict


class Play(State):
    """
    Screen of the game where the user needs to
    survive as much as possible
    """
    def __init__(self):
        super().__init__()
        self.map = Map()
        self.delay_to_game_over = 0

        self.load_graphics = graphics_dict['title']
        self.loading = True

        self.time = pygame.time.get_ticks()
        self.time_finish_load = 0
        self.last_transition_title_time = 0
        self.counter_load = 0

        loadbar_left = SCREEN_WIDTH/2 - LOADBAR_WIDTH/2
        loadbar_top = 4*SCREEN_HEIGHT/5
        self.loadbar_rect = pygame.Rect(loadbar_left, loadbar_top, LOADBAR_WIDTH, LOADBAR_HEIGHT)

    def update(self):
        """
        Updates the game
        """
        self.map.update()

        if self.loading:
            self.time = pygame.time.get_ticks()
            if self.time - self.last_transition_title_time >= TITLE_FRAMERATE:
                self.last_transition_title_time = self.time
                self.counter_load += 1
                if self.counter_load > 4:
                    self.counter_load = 0

            self.time_finish_load += 1
            if self.time_finish_load == LOADING_TIME:
                self.loading = False
                self.time_finish_load = 0

        if not self.map.get_player().is_alive():
            self.delay_to_game_over += 1
        if self.delay_to_game_over == PLAY_TO_OVER_DELAY:
            self.custom_value = self.map.get_player().get_score()
            self.next = 'OVER'
            self.clear_window = True
            pygame.mixer.music.stop()
            pygame.mixer.music.unload()

    def draw(self, screen):
        """
        Draws the game
        """
        if self.loading:
            screen.blit_rel(self.load_graphics[self.counter_load], (0, 0))

            filling_rect = pygame.Rect(self.loadbar_rect)
            loaded_frac = self.time_finish_load/LOADING_TIME
            filling_rect.width = int(loaded_frac*filling_rect.width)
            pygame.draw.rect(screen, WHITE, self.loadbar_rect, 1)
            pygame.draw.rect(screen, WHITE, filling_rect)
        else:
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
