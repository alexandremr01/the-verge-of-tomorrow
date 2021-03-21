import pygame
import numpy as np
from data.constants import CHUNK_SIZE, CHUNK_ARRAY, TILE_SIZE, TILE_ARRAY, RENDER_STEPS


class Chunk:
    def __init__(self, position):
        self.position = position
        self.tilegrid = np.array([[]])
        self.is_rendering = True
        self.render_step = 0

    def is_rendered(self):
        return self.tilegrid is not None

    def render(self, generator):
        ref = self.position * CHUNK_SIZE - CHUNK_ARRAY / 2 + TILE_ARRAY / 2 + \
              np.array([0, CHUNK_SIZE // RENDER_STEPS]) * self.render_step
        new_load = np.array([[generator.noise2d(ref[0] + TILE_SIZE * i,
                                                ref[1] + TILE_SIZE * j)
                              for j in range(CHUNK_SIZE // TILE_SIZE)]
                             for i in range((CHUNK_SIZE // TILE_SIZE) // RENDER_STEPS)])
        if self.render_step == 0:
            self.tilegrid = new_load
        else:
            self.tilegrid = np.concatenate((self.tilegrid, new_load), axis=0)
        self.decode_tilegrid()
        self.render_step += 1
        if self.render_step is RENDER_STEPS:
            self.is_rendering = False
            self.render_step = 0

    def decode_tilegrid(self):
        row = ((CHUNK_SIZE // TILE_SIZE) // RENDER_STEPS) * self.render_step
        for i in range((CHUNK_SIZE // TILE_SIZE) // RENDER_STEPS):
            for j in range(CHUNK_SIZE // TILE_SIZE):
                if self.tilegrid[row + i][j] < - 0.2:
                    self.tilegrid[row + i][j] = 0
                elif - 0.2 <= self.tilegrid[row + i][j] < 0.1:
                    self.tilegrid[row + i][j] = 1
                else:
                    self.tilegrid[row + i][j] = 2

    def de_render(self):
        self.tilegrid = None

    def draw(self, surface, position, tiles):
        for i in range(CHUNK_SIZE // TILE_SIZE):
            for j in range(CHUNK_SIZE // TILE_SIZE):
                surface.blit(tiles.terrain[self.tilegrid[i][j]].sprite.get_image(),
                             position + np.array([i, j]) * TILE_SIZE)
