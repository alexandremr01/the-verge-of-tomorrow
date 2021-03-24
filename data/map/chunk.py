import pygame
import numpy as np
from data.constants import CHUNK_SIZE, CHUNK_ARRAY, TILE_SIZE, RENDER_STEPS, CHUNK_TILE_RATIO, CHUNK_TILE_RATIO_STEPS


class Chunk:
    def __init__(self, position):
        self.position = position
        self.topleft = position * CHUNK_SIZE - CHUNK_ARRAY / 2
        self.tilegrid = None
        self.surface = None
        self.is_rendering = True
        self.render_step = 0

    def is_rendered(self):
        return self.tilegrid is not None

    def de_render(self):
        self.tilegrid = None
        self.surface = None

    def render(self, generator, tiles):
        self.is_rendering = True
        start_position = self.topleft + np.array([0, CHUNK_SIZE // RENDER_STEPS * self.render_step])
        new_load = np.array([[generator.noise2d((start_position[0] + TILE_SIZE * j) / TILE_SIZE,
                                                -(start_position[1] + TILE_SIZE * i) / TILE_SIZE)
                              for j in range(CHUNK_TILE_RATIO)]
                             for i in range(CHUNK_TILE_RATIO_STEPS)])
        if self.render_step == 0:
            self.tilegrid = new_load
            self.surface = pygame.Surface(CHUNK_ARRAY)
        else:
            self.tilegrid = np.concatenate((self.tilegrid, new_load), axis=0)
        self.decode_and_draw(CHUNK_TILE_RATIO_STEPS * self.render_step, tiles)
        self.render_step += 1
        if self.render_step is RENDER_STEPS:
            self.is_rendering = False
            self.render_step = 0

    def decode_and_draw(self, row, tiles):
        for i in range(CHUNK_TILE_RATIO_STEPS):
            for j in range(CHUNK_TILE_RATIO):
                if self.tilegrid[row + i][j] < - 0.2:
                    self.tilegrid[row + i][j] = 0
                elif - 0.2 <= self.tilegrid[row + i][j] < 0.1:
                    self.tilegrid[row + i][j] = 1
                else:
                    self.tilegrid[row + i][j] = 2

                self.surface.blit(tiles.terrain[self.tilegrid[row + i][j]].sprite.get_image(),
                                  np.array([row + i, j]) * TILE_SIZE)

