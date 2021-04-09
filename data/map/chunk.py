import pygame
import numpy as np
from data.utils import compare
from data.constants import CHUNK_SIZE, CHUNK_ARRAY, TILE_SIZE, RENDER_STEPS, CHUNK_TILE_RATIO, CHUNK_TILE_RATIO_STEPS


class Chunk:
    def __init__(self, position):
        self.position = position
        self.topleft = position * CHUNK_SIZE - CHUNK_ARRAY / 2
        self.tilegrid = None
        self.structuregrid = None
        self.structures = None
        self.seed = np.random.randint(0, 10000)
        self.surface = None
        self.is_rendering = True
        self.terrain_step = 0
        self.terrain_steps = RENDER_STEPS
        self.structures_step = -1
        self.structures_steps = 0
        self.draw_step = 0
        self.draw_steps = RENDER_STEPS

    def is_rendered(self):
        return self.tilegrid is not None

    def de_render(self):
        self.tilegrid = None
        self.structuregrid = None
        self.surface = None
        self.structures = None
        self.structures_step = -1
        self.terrain_step = self.draw_step = 0

    def generate_structure_variables(self, number_of_structures):
        self.structuregrid = np.zeros((CHUNK_TILE_RATIO, CHUNK_TILE_RATIO))
        positions = np.array([[0.25, 0.25], [0.75, 0.75], [0.25, 0.75], [0.75, 0.25]]) * CHUNK_TILE_RATIO
        positions = np.concatenate((positions.astype(int), [[1], [2], [3], [4]]), axis=1)
        np.random.seed(self.seed)
        positions = np.take(positions,
                            np.random.choice([0, 1, 2, 3], size=number_of_structures, replace=False),
                            axis=0)
        self.structures = {}
        for position in positions:
            structure_seed = self.seed + position[2]
            np.random.seed(structure_seed)
            number_of_directions = np.random.choice([1, 2, 3, 4], p=[0.35, 0.35, 0.2, 0.1])
            number_of_directions = 4
            np.random.seed(structure_seed)
            directions = np.take([[1, 1, 11], [-1, 1, 12], [-1, -1, 13], [1, -1, 14]],
                                 np.random.choice(np.array([0, 1, 2, 3]), size=number_of_directions,
                                                  replace=False), axis=0)
            generation_variables = []
            for direction in directions:
                direction_seed = structure_seed + direction[2]
                np.random.seed(direction_seed)
                width = np.random.randint(6, CHUNK_TILE_RATIO / 4 - 1)
                np.random.seed(direction_seed + 5)
                height = np.random.randint(6, CHUNK_TILE_RATIO / 4 - 1)
                generation_variables.append([direction[:2], [width, height]])
            self.structures[tuple(position[:2])] = generation_variables

    def generate_terrain(self, generator):
        start_position = self.topleft + np.array([0, CHUNK_SIZE // self.terrain_steps * self.terrain_step])
        new_load = np.array([[(generator.noise2d((start_position[0] / TILE_SIZE + j)/2.8,
                                                 -(start_position[1] / TILE_SIZE + i)/2.8) + 1) / 2
                              for j in range(CHUNK_TILE_RATIO)]
                             for i in range(CHUNK_TILE_RATIO_STEPS)])
        if self.terrain_step == 0:
            self.tilegrid = new_load
            self.surface = pygame.Surface(CHUNK_ARRAY)
        else:
            self.tilegrid = np.concatenate((self.tilegrid, new_load), axis=0)

    def check_wall_collision(self, x, y, tiles):
        if tiles.is_what(self.structuregrid[x + 1][y], "FLOOR"):
            if tiles.is_what(self.structuregrid[x][y + 1], "FLOOR"):
                self.structuregrid[x][y] = tiles.code["WALL_BOTTOM_RIGHT"]
            else:
                self.structuregrid[x][y] = tiles.code["WALL_TOP_RIGHT"]
        else:
            if tiles.is_what(self.structuregrid[x][y + 1], "FLOOR"):
                self.structuregrid[x][y] = tiles.code["WALL_BOTTOM_LEFT"]
            else:
                self.structuregrid[x][y] = tiles.code["WALL_TOP_LEFT"]

    def generate_structure(self, tiles):
        position = 0
        for s in enumerate(self.structures):
            if s[0] == self.structures_step:
                position = s[1]
                break

        for direction, length in self.structures[position]:
            x_direction, y_direction = direction
            width, height = length

            # Set floor
            for i in range(-1, width):
                for j in range(-1, height):
                    x = position[0] + x_direction * i
                    y = position[1] + y_direction * j
                    self.structuregrid[x][y] = tiles.code["CHECKERED_PLAIN"]

            # Set left and right walls
            for i in [-2, width]:
                for j in range(-1, height):
                    x = position[0] + x_direction * i
                    y = position[1] + y_direction * j
                    if self.structuregrid[x][y] == tiles.code["WALL_TOP_BOTTOM"]:
                        self.check_wall_collision(x, y, tiles)
                    elif not tiles.is_what(self.structuregrid[x][y], "FLOOR"):
                        self.structuregrid[x][y] = tiles.code["WALL_LEFT_RIGHT"]

            # Set top and bottom walls
            for j in [-2, height]:
                for i in range(-1, width):
                    x = position[0] + x_direction * i
                    y = position[1] + y_direction * j
                    if self.structuregrid[x][y] == tiles.code["WALL_LEFT_RIGHT"]:
                        self.check_wall_collision(x, y, tiles)
                    elif not tiles.is_what(self.structuregrid[x][y], "FLOOR"):
                        self.structuregrid[x][y] = tiles.code["WALL_TOP_BOTTOM"]

            # Set Corners
            for i in [-2, width]:
                for j in [-2, height]:
                    x = position[0] + x_direction * i
                    y = position[1] + y_direction * j
                    if tiles.is_what(self.structuregrid[x][y], "TERRAIN"):
                        if tiles.is_what(self.structuregrid[x + 1][y], "WALL"):
                            if tiles.is_what(self.structuregrid[x][y + 1], "WALL"):
                                self.structuregrid[x][y] = tiles.code["WALL_TOP_LEFT"]
                            else:
                                self.structuregrid[x][y] = tiles.code["WALL_BOTTOM_LEFT"]
                        else:
                            if tiles.is_what(self.structuregrid[x][y + 1], "WALL"):
                                self.structuregrid[x][y] = tiles.code["WALL_TOP_RIGHT"]
                            else:
                                self.structuregrid[x][y] = tiles.code["WALL_BOTTOM_RIGHT"]

    def render(self, generator, tiles):
        self.is_rendering = True
        if self.structures_step == -1:
            np.random.seed(self.seed)
            number_of_structures = int(np.random.choice([0, 1, 2, 3, 4], p=[0.6, 0.2, 0.1, 0.05, 0.05]))
            number_of_structures = 4
            if number_of_structures != 0:
                self.generate_structure_variables(number_of_structures)
            self.structures_steps = number_of_structures
            self.structures_step += 1
        else:
            if self.terrain_step is not self.terrain_steps:
                self.generate_terrain(generator)
                self.terrain_step += 1
            else:
                if self.structures_step is not self.structures_steps:
                    self.generate_structure(tiles)
                    self.structures_step += 1
                else:
                    if self.draw_step is not self.draw_steps:
                        self.draw(tiles)
                        self.draw_step += 1
                    else:
                        self.is_rendering = False

    def draw(self, tiles):
        row = CHUNK_TILE_RATIO_STEPS * self.draw_step
        for i in range(CHUNK_TILE_RATIO_STEPS):
            for j in range(CHUNK_TILE_RATIO):
                self.decode(row + i, j, tiles)
                self.surface.blit(tiles.sprites[self.tilegrid[row + i][j]].sprite.get_image(),
                                  np.array([row + i, j]) * TILE_SIZE)

    def decode(self, i, j, tiles):
        if self.structuregrid is None or self.structuregrid[i][j] == 0:
            terrain_noise = self.tilegrid[i][j]
            # if self.structuregrid is not None:
            #     terrain_noise = terrain_noise + np.power(terrain_noise, 3) * (0.68 - terrain_noise)
            if 0 <= terrain_noise - 0.1 < 0.15:
                self.tilegrid[i][j] = compare(noise_value=terrain_noise, starting_value=0.1, interval_percentage=0.15,
                                              slices=[tiles.code["GRASS_DARKLEAFS_1"],
                                                      tiles.code["GRASS_DARKLEAFS_2"]],
                                              percentages=[0.6, 0.4])
            elif 0 <= terrain_noise - 0.25 <= 0.45:
                self.tilegrid[i][j] = tiles.code["GRASS_PLAIN"]
            elif 0 <= terrain_noise - 0.7 < 0.3:
                self.tilegrid[i][j] = compare(noise_value=terrain_noise, starting_value=0.7, interval_percentage=0.3,
                                              slices=[tiles.code["GRASS_BRIGHTLEAFS_4"],
                                                      tiles.code["GRASS_BRIGHTLEAFS_3"],
                                                      tiles.code["GRASS_BRIGHTLEAFS_2"],
                                                      tiles.code["GRASS_BRIGHTLEAFS_1"]],
                                              percentages=[0.05, 0.1, 0.15, 0.7])
            else:
                self.tilegrid[i][j] = tiles.code["ROCK"]
        elif tiles.is_what(self.structuregrid[i][j], "FLOOR"):
            floor_noise = self.tilegrid[i][j]
            if 0 <= floor_noise - 0.1 < 0.2:
                self.tilegrid[i][j] = compare(noise_value=floor_noise, starting_value=0.1, interval_percentage=0.2,
                                              slices=[tiles.code["GRASS_BRIGHTLEAFS_1"],
                                                      tiles.code["GRASS_BRIGHTLEAFS_2"],
                                                      tiles.code["CHECKERED_GRASS_3"],
                                                      tiles.code["CHECKERED_GRASS_2"],
                                                      tiles.code["CHECKERED_GRASS_1"]],
                                              percentages=[0.1, 0.2, 0.2, 0.25, 0.25])
            elif 0 <= floor_noise - 0.6 < 0.4:
                self.tilegrid[i][j] = compare(noise_value=floor_noise, starting_value=0.6, interval_percentage=0.4,
                                              slices=[tiles.code["CHECKERED_BROKEN_2"],
                                                      tiles.code["CHECKERED_BROKEN_1"]],
                                              percentages=[0.4, 0.6])
            else:
                self.tilegrid[i][j] = tiles.code["CHECKERED_PLAIN"]
        else:
            self.tilegrid[i][j] = self.structuregrid[i][j]
