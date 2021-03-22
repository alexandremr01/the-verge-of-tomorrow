import pygame
import numpy as np
from data.constants import CHUNK_SIZE, CHUNK_ARRAY, TILE_SIZE, TILE_ARRAY, RENDER_STEPS, CHUNK_TILE_RATIO


class Chunk:
    def __init__(self, position):
        self.position = position
        self.tilegrid = None
        self.is_rendering = True
        self.render_step = 0

    def is_rendered(self):
        return self.tilegrid is not None

    def render(self, generator):
        self.is_rendering = True
        ref = self.position * CHUNK_SIZE - CHUNK_ARRAY / 2 + TILE_ARRAY / 2 + \
              np.array([0, CHUNK_SIZE // RENDER_STEPS]) * self.render_step
        new_load = np.array([[generator.noise2d((ref[0] + TILE_SIZE * j) / TILE_SIZE,
                                                -(ref[1] + TILE_SIZE * i) / TILE_SIZE)
                              for j in range(CHUNK_TILE_RATIO)]
                             for i in range(CHUNK_TILE_RATIO // RENDER_STEPS)])
        if self.render_step == 0:
            self.tilegrid = new_load
        else:
            self.tilegrid = np.concatenate((self.tilegrid, new_load), axis=0)
        self.decode_tilegrid(CHUNK_TILE_RATIO // RENDER_STEPS * self.render_step)
        self.render_step += 1
        if self.render_step is RENDER_STEPS:
            self.is_rendering = False
            self.render_step = 0

    def decode_tilegrid(self, row):
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
        for i in range(CHUNK_TILE_RATIO):
            for j in range(CHUNK_TILE_RATIO):
                surface.blit(tiles.terrain[self.tilegrid[i][j]].sprite.get_image(),
                             position + np.array([i, j]) * TILE_SIZE)
