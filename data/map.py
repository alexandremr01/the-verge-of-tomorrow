"""
Class supposed to contain entities that will be rendered at game state
"""

import pygame
import numpy

from .constants import SCREEN_HEIGHT, SCREEN_WIDTH
from .components.sprite import SpriteSheet, Sprite

class RandomMap:
    """
    For testing purposes
    """
    def __init__(self, spritesheet):
        """
        type spritesheet : SpriteSheet
        """
        self.map = []
        num_rows = SCREEN_HEIGHT // spritesheet.get_resolution()
        num_columns = SCREEN_WIDTH // spritesheet.get_resolution()
        tile_num = numpy.random.randint(spritesheet.get_size(), size=(num_rows, num_columns)) # random map
        # tile_num = numpy.ones((num_rows, num_columns), dtype=int) # one tile
        for i in range(num_rows):
            for j in range(num_columns):
                sprite = Sprite(((i * spritesheet.resolution + (spritesheet.resolution // 2)), 
                                  (j * spritesheet.resolution + (spritesheet.resolution // 2))),
                                 spritesheet.get_image(tile_num[i][j]))
                self.map.append(sprite)

    def draw(self, surface):
        for tile in self.map:
            surface.blit(tile.get_image(), tile.get_position())
