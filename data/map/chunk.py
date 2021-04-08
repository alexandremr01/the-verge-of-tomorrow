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
            self.gen_structures(int(100000 * (generator.noise2d(self.topleft[0], self.topleft[1]) + 1)), tiles)
            self.is_rendering = False
            self.render_step = 0

    def blit(self, tiles, x, y):
        self.surface.blit(tiles[self.tilegrid[x][y]].sprite.get_image(),
                          np.array([x, y]) * TILE_SIZE)

    def gen_structures(self, seed, tiles):
        np.random.seed(seed)
        if np.random.rand() < 1:
            np.random.seed(seed)
            number_of_generators = np.random.choice([1, 2, 3, 4], p=[0.5, 0.3, 0.15, 0.05])
            positions = (np.array([[0.25, 0.25], [0.75, 0.75], [0.25, 0.75], [0.75, 0.25]]) * CHUNK_TILE_RATIO)
            positions = np.concatenate((positions.astype(int), np.array([[1], [2], [3], [4]])), axis=1)
            np.random.seed(seed)
            positions = np.take(positions,
                                np.random.choice(np.array([0, 1, 2, 3]), size=number_of_generators, replace=False),
                                axis=0)

            for position in positions:
                position_seed = seed + position[2]
                np.random.seed(position_seed)
                number_of_directions = np.random.choice([1, 2, 3, 4], p=[0.35, 0.35, 0.2, 0.1])
                np.random.seed(position_seed)
                directions = np.take(np.array([[1, 1, 11], [-1, 1, 12], [-1, -1, 13], [1, -1, 14]]),
                                     np.random.choice(np.array([0, 1, 2, 3]), size=number_of_directions, replace=False),
                                     axis=0)

                for direction in directions:
                    direction_seed = position_seed + direction[2]
                    np.random.seed(direction_seed)
                    x = np.random.randint(6, CHUNK_TILE_RATIO / 4 - 1)
                    np.random.seed(direction_seed + 1)
                    y = np.random.randint(6, CHUNK_TILE_RATIO / 4 - 1)
                    for i in range(-1, x):
                        for j in range(-1, y):
                            x_entry = position[0] + direction[0] * i
                            y_entry = position[1] + direction[1] * j
                            self.tilegrid[x_entry][y_entry] = -(self.tilegrid[x_entry][y_entry] % 3) - 1
                            self.blit(tiles.structures, x_entry, y_entry)

                    # Draw left and right walls
                    for i in [-2, x]:
                        for j in range(-1, y):
                            x_entry = position[0] + direction[0] * i
                            y_entry = position[1] + direction[1] * j
                            if not (-6 <= self.tilegrid[x_entry][y_entry] <= -1) and not self.tilegrid[x_entry][y_entry] == -8:
                                self.tilegrid[x_entry][y_entry] = -7
                                self.blit(tiles.structures, x_entry, y_entry)
                            elif self.tilegrid[x_entry][y_entry] == -8:
                                if -6 <= self.tilegrid[x_entry + 1][y_entry] <= -1:
                                    if -6 <= self.tilegrid[x_entry][y_entry + 1] <= -1:
                                        self.tilegrid[x_entry][y_entry] = -9  # BOTTOM RIGHT
                                    else:
                                        self.tilegrid[x_entry][y_entry] = -10  # TOP RIGHT
                                else:
                                    if -6 <= self.tilegrid[x_entry][y_entry + 1] <= -1:
                                        self.tilegrid[x_entry][y_entry] = -11  # BOTTOM LEFT
                                    else:
                                        self.tilegrid[x_entry][y_entry] = -12  # TOP LEFT
                                self.blit(tiles.structures, x_entry, y_entry)

                    # Draw top and bottom walls
                    for j in [-2, y]:
                        for i in range(-1, x):
                            x_entry = position[0] + direction[0] * i
                            y_entry = position[1] + direction[1] * j
                            if not (-6 <= self.tilegrid[x_entry][y_entry] <= -1) and not self.tilegrid[x_entry][y_entry] == -7:
                                self.tilegrid[x_entry][y_entry] = -8
                                self.blit(tiles.structures, x_entry, y_entry)
                            elif self.tilegrid[x_entry][y_entry] == -7:
                                if -6 <= self.tilegrid[x_entry + 1][y_entry] <= -1:
                                    if -6 <= self.tilegrid[x_entry][y_entry + 1] <= -1:
                                        self.tilegrid[x_entry][y_entry] = -9  # BOTTOM RIGHT
                                    else:
                                        self.tilegrid[x_entry][y_entry] = -10  # TOP RIGHT
                                else:
                                    if -6 <= self.tilegrid[x_entry][y_entry + 1] <= -1:
                                        self.tilegrid[x_entry][y_entry] = -11  # BOTTOM LEFT
                                    else:
                                        self.tilegrid[x_entry][y_entry] = -12  # TOP LEFT
                                self.blit(tiles.structures, x_entry, y_entry)

                    # Draw Corners
                    for i in [-2, x]:
                        for j in [-2, y]:
                            x_entry = position[0] + direction[0] * i
                            y_entry = position[1] + direction[1] * j
                            if self.tilegrid[x_entry][y_entry] >= 0:
                                if self.tilegrid[x_entry + 1][y_entry] < 0:
                                    if self.tilegrid[x_entry][y_entry + 1] < 0:
                                        self.tilegrid[x_entry][y_entry] = -12  # TOP LEFT
                                    else:
                                        self.tilegrid[x_entry][y_entry] = -11  # BOTTOM LEFT
                                else:
                                    if self.tilegrid[x_entry][y_entry + 1] < 0:
                                        self.tilegrid[x_entry][y_entry] = -10  # TOP RIGHT
                                    else:
                                        self.tilegrid[x_entry][y_entry] = -9  # BOTTOM RIGHT
                                self.blit(tiles.structures, x_entry, y_entry)


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

                self.blit(tiles.terrain, row + i, j)


