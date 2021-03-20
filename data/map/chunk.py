import pygame
import numpy as np
from data.constants import CHUNK_SIZE, CHUNK_ARRAY, TILE_SIZE, TILE_ARRAY


class Chunk:
    def __init__(self, position):
        self.position = position
        self.tilegrid = None

    def is_rendered(self):
        return self.tilegrid is not None

    def render(self, generator):
        ref = self.position * CHUNK_SIZE - CHUNK_ARRAY / 2 + TILE_ARRAY / 2
        self.tilegrid = np.array([[generator.noise2d(ref[0] + TILE_SIZE * i,
                                                     ref[1] + TILE_SIZE * j)
                                   for i in range(CHUNK_SIZE // TILE_SIZE)]
                                  for j in range(CHUNK_SIZE // TILE_SIZE)])
        self.decode_tilegrid()

    def decode_tilegrid(self):
        for i in range(CHUNK_SIZE // TILE_SIZE):
            for j in range(CHUNK_SIZE // TILE_SIZE):
                if self.tilegrid[i][j] < - 0.2:
                    self.tilegrid[i][j] = 0
                elif - 0.2 <= self.tilegrid[i][j] < 0.5:
                    self.tilegrid[i][j] = 1
                else:
                    self.tilegrid[i][j] = 2

    def de_render(self):
        self.tilegrid = None

    def draw(self, surface, position, tiles):
        for i in range(CHUNK_SIZE // TILE_SIZE):
            for j in range(CHUNK_SIZE // TILE_SIZE):
                surface.blit(tiles.terrain[self.tilegrid[i][j]].sprite.get_image(),
                             position + np.array([i, j]) * TILE_SIZE)
