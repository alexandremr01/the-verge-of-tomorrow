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
        new_load = np.array([[generator.noise2d((start_position[0] / TILE_SIZE + j) / 3,
                                                -(start_position[1] / TILE_SIZE + i) / 3) + 1.0
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
                terrainnoise = self.tilegrid[row + i][j]

                if 0.15 <= terrainnoise < 0.195:
                    self.tilegrid[row + i][j] = 7
                else:
                    if 0.3 <= terrainnoise < 0.7:
                        if 0.3 <= terrainnoise < 0.39:
                            self.tilegrid[row + i][j] = 1
                        elif 0.39 <= terrainnoise < 0.45:
                            self.tilegrid[row + i][j] = 2
                        elif 0.45 <= terrainnoise < 0.53:
                            self.tilegrid[row + i][j] = 3
                        elif 0.53 <= terrainnoise < 0.61:
                            self.tilegrid[row + i][j] = 4
                        elif 0.61 <= terrainnoise < 0.67:
                            self.tilegrid[row + i][j] = 5
                        else:
                            self.tilegrid[row + i][j] = 6
                    else:
                        self.tilegrid[row + i][j] = 0

                self.surface.blit(tiles.terrain[self.tilegrid[row + i][j]].sprite.get_image(),
                                  np.array([row + i, j]) * TILE_SIZE)

