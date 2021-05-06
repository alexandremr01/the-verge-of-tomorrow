import pygame
import numpy as np
from data.components.item import ItemGenerator
from data.utils import compare
from data.constants import CHUNK_SIZE, CHUNK_ARRAY, TILE_SIZE, RENDER_STEPS, TILE_NUMBER
from data.map.tile import *
from data.map.chunk_generator import *


class Chunk:
    """
    Class responsible for carrying terrain and structures data.
    """

    def __init__(self, position):
        self.position = position
        self.topleft = position * CHUNK_SIZE - CHUNK_ARRAY / 2
        self.tilegrid = None
        self.structuregrid = None
        self.structures = None
        self.seed = np.random.randint(0, 10000)
        self.surface = None
        self.surface_night = None
        self.is_rendering = True
        self.terrain_step = 0
        self.terrain_steps = 8
        self.structures_step = -1
        self.structures_steps = 0
        self.draw_step = 0
        self.draw_steps = RENDER_STEPS
        self.item_generator = ItemGenerator()

    def is_unloaded(self):
        return self.tilegrid is None

    def is_rendered(self):
        return not self.is_rendering

    def de_render(self):
        self.tilegrid = None
        self.structuregrid = None
        self.surface = None
        self.surface_night = None
        self.structures = None
        self.structures_step = -1
        self.terrain_step = self.draw_step = 0

    def generate_structure_variables(self, number_of_structures):
        self.structuregrid = np.zeros((TILE_NUMBER, TILE_NUMBER))
        self.structures = gen_structure_info(self.seed, number_of_structures)

    def generate_terrain(self, generator):
        load = gen_terrain_load(generator, self.topleft, self.terrain_step)
        if self.terrain_step == 0:
            self.tilegrid = load
            self.surface = pygame.Surface(CHUNK_ARRAY)
            self.surface_night = pygame.Surface(CHUNK_ARRAY)
        else:
            self.tilegrid = np.concatenate((self.tilegrid, load), axis=0)

    def generate_structure(self):
        position = [*self.structures][self.structures_step]  # Gets next structure position to generate

        interior_floor = []
        border_floor = []
        horizontal_walls = []
        vertical_walls = []
        corner_walls = []
        opening_walls = []

        build_floor(self.structuregrid, self.structures, position, interior_floor, border_floor)
        build_walls(self.structuregrid, border_floor, horizontal_walls, vertical_walls, corner_walls)

        # Sorting list of walls to help in creating openings
        horizontal_walls.sort(key=lambda element: (element[0], element[1]))
        vertical_walls.sort(key=lambda element: (element[1], element[0]))

        create_openings(self.seed, self.structuregrid, self.structures, position,
                        horizontal_walls, vertical_walls, opening_walls)
        cast_shadows(self.seed, self.structuregrid, horizontal_walls, vertical_walls, corner_walls, opening_walls)

        generate_items(self.seed, self.structuregrid, self.structures, position, interior_floor)

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
                    self.generate_structure()
                    self.structures_step += 1
                else:
                    if self.draw_step is not self.draw_steps:
                        self.draw(tiles)
                        self.draw_step += 1
                    else:
                        self.is_rendering = False

    def blit(self, i, j, tiles, grid):
        self.surface.blit(tiles.tilesdict[grid[i][j]].sprite.get_image(),
                          np.array([j, i]) * TILE_SIZE)
        self.surface_night.blit(tiles.tilesdict[grid[i][j]].sprite_night.get_image(),
                                np.array([j, i]) * TILE_SIZE)

    def draw(self, tiles):
        row = TILE_NUMBER // self.draw_steps * self.draw_step
        for i in range(TILE_NUMBER // self.draw_steps):
            for j in range(TILE_NUMBER):
                self.decode(row + i, j)
                self.blit(row + i, j, tiles, self.tilegrid)
                if self.structuregrid is not None and is_what(self.structuregrid[row + i][j], ITEM):
                    self.blit(row + i, j, tiles, self.structuregrid)

    def decode(self, i, j):
        if self.structuregrid is None or self.structuregrid[i][j] == 0:
            terrain_noise = self.tilegrid[i][j]
            if 0 <= terrain_noise - 0.1 < 0.15:
                self.tilegrid[i][j] = compare(noise_value=terrain_noise, starting_value=0.1, interval_percentage=0.15,
                                              slices=[GRASS_DARKLEAFS_1,
                                                      GRASS_DARKLEAFS_2],
                                              percentages=[0.6, 0.4])
            elif 0 <= terrain_noise - 0.25 <= 0.45:
                self.tilegrid[i][j] = GRASS_PLAIN
            elif 0 <= terrain_noise - 0.7 < 0.3:
                self.tilegrid[i][j] = compare(noise_value=terrain_noise, starting_value=0.7, interval_percentage=0.3,
                                              slices=[GRASS_BRIGHTLEAFS_4,
                                                      GRASS_BRIGHTLEAFS_3,
                                                      GRASS_BRIGHTLEAFS_2,
                                                      GRASS_BRIGHTLEAFS_1],
                                              percentages=[0.05, 0.1, 0.15, 0.7])
            else:
                self.tilegrid[i][j] = ROCK
        elif (is_what(self.structuregrid[i][j], FLOOR) or is_what(self.structuregrid[i][j], ITEM)) \
                and not is_what(self.structuregrid[i][j], FLOOR_SHADOW):
            floor_noise = self.tilegrid[i][j]
            if 0 <= floor_noise - 0.1 < 0.2:
                self.tilegrid[i][j] = compare(noise_value=floor_noise, starting_value=0.1, interval_percentage=0.2,
                                              slices=[GRASS_BRIGHTLEAFS_1,
                                                      GRASS_BRIGHTLEAFS_2,
                                                      CHECKERED_GRASS_3,
                                                      CHECKERED_GRASS_2,
                                                      CHECKERED_GRASS_1],
                                              percentages=[0.1, 0.2, 0.2, 0.25, 0.25])
            elif 0 <= floor_noise - 0.6 < 0.4:
                self.tilegrid[i][j] = compare(noise_value=floor_noise, starting_value=0.6, interval_percentage=0.4,
                                              slices=[CHECKERED_BROKEN_2,
                                                      CHECKERED_BROKEN_1],
                                              percentages=[0.4, 0.6])
            else:
                self.tilegrid[i][j] = CHECKERED_PLAIN
        else:
            self.tilegrid[i][j] = self.structuregrid[i][j]
