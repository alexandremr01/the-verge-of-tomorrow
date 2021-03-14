"""
This module contains an extension of the
pygame surface class, which adds a corner
(left, top) position which may be different
of (0, 0)
"""

import pygame
import numpy as np

class ScreenSurface(pygame.Surface):
    """
    Extension of pygame surface which may be used
    as a "cutout" of a bigger picture
    """
    def __init__(self, screen_rect):
        super().__init__((screen_rect.width, screen_rect.height))

        self.screen_rect = screen_rect
        self.screen_corner = np.array([screen_rect.left, screen_rect.top])
        self.screen_dimensions = np.array([screen_rect.width, screen_rect.height])

    def center_on_player(self, player_position):
        """
        Changes its parameters so that the screen is
        a bigger picture cutout with the player at
        exactly its center
        """
        self.screen_corner = player_position - self.screen_dimensions/2
        self.screen_rect.left = self.screen_corner[0]
        self.screen_rect.top = self.screen_corner[1]

    def reset_corner(self):
        """
        Changes back its top left corner position
        to (0, 0)
        """
        self.screen_rect.left, self.screen_rect.right = 0, 0
        self.screen_corner[0], self.screen_corner[1] = 0, 0

    def blit_rel(self, sprite, sprite_corner):
        """
        Includes in ScreenSurface a sprite
        with its top left corner located at
        sprite_corner (given with respect
        to ScreenSurface)
        """
        super().blit(sprite, sprite_corner)

    def blit(self, sprite, sprite_corner):
        """
        Includes in ScreenSurface a sprite
        with its top left corner located
        at sprite_corner (given with
        respect to the bigger picture)
        """
        if isinstance(sprite_corner, pygame.Rect):
            sprite_corner_in_screen = pygame.Rect(sprite_corner)
            sprite_corner_in_screen.left -= self.screen_corner[0]
            sprite_corner_in_screen.top -= self.screen_corner[1]
        else:
            sprite_corner_in_screen = sprite_corner - self.screen_corner

        super().blit(sprite, sprite_corner_in_screen)
