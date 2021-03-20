import pygame
import numpy as np
from .constants import CHUNK_SIZE, CHUNK_ARRAY, TILE_SIZE, TILE_ARRAY


class Chunk:
    def __init__(self, position):
        self.position = position
        self.tilegrid = None

    def is_rendered(self):
        return self.tilegrid is not None

    def render(self, generator):
        ref = self.position * CHUNK_SIZE - CHUNK_ARRAY/2 + TILE_ARRAY/2
        self.tilegrid = [[generator.noise2d(ref[0] + TILE_SIZE * i,
                                            ref[1] + TILE_SIZE * j)
                          for i in range(CHUNK_SIZE // TILE_SIZE)]
                         for j in range(CHUNK_SIZE // TILE_SIZE)]
        self.decode_tilegrid()

    def decode_tilegrid(self):
        pass

    def de_render(self):
        self.tilegrid = None

    def draw(self, surface, position):
        pass
