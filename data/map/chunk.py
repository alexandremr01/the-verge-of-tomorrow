import pygame
import numpy as np
from data.components.item import ItemGenerator
from data.utils import compare
from data.constants import CHUNK_SIZE, CHUNK_ARRAY, TILE_SIZE, DRAW_RENDER_STEPS, TERRAIN_BUILD_STEPS, TILE_NUMBER
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
        self.terrain_steps = TERRAIN_BUILD_STEPS
        self.structures_step = -1
        self.structures_steps = 0
        self.draw_step = 0
        self.draw_steps = DRAW_RENDER_STEPS
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

    def initialize_chunk_variables(self):
        self.surface = pygame.Surface(CHUNK_ARRAY)
        self.surface_night = pygame.Surface(CHUNK_ARRAY)

        number_of_structures = randchoice(self.seed, array=5, p=[0.6, 0.2, 0.1, 0.05, 0.05])
        if number_of_structures > 0:
            self.structuregrid = np.zeros((TILE_NUMBER, TILE_NUMBER))
            self.structures = gen_structure_info(self.seed, number_of_structures)
        self.structures_steps = number_of_structures
        self.terrain_step = 0
        self.draw_step = 0

    def generate_terrain(self, generator):
        load = gen_terrain_load(generator, self.topleft, self.terrain_step)
        if self.terrain_step == 0:
            self.tilegrid = load
        else:
            self.tilegrid = np.concatenate((self.tilegrid, load), axis=0)

    def generate_structure(self):
        position = [*self.structures][self.structures_step]  # Gets next structure position to generate

        # Helpful lists
        interior_floor = []
        border_floor = []
        horizontal_walls = []
        vertical_walls = []
        corner_walls = []
        horizontal_opening_walls = []
        vertical_opening_walls = []

        build_floor(self.structuregrid, self.structures, position, interior_floor, border_floor)
        build_walls(self.structuregrid, border_floor, horizontal_walls, vertical_walls, corner_walls)

        # Sorting list of walls to help in creating openings
        horizontal_walls.sort(key=lambda element: (element[0], element[1]))
        vertical_walls.sort(key=lambda element: (element[1], element[0]))

        create_openings(self.seed, self.structuregrid, self.structures, position,
                        horizontal_walls, vertical_walls, horizontal_opening_walls, vertical_opening_walls)
        cast_shadows(self.seed, self.structuregrid, horizontal_walls, vertical_walls, corner_walls,
                     horizontal_opening_walls, vertical_opening_walls)

        generate_items(self.seed, self.structuregrid, self.structures, position, interior_floor)

    def render(self, generator, tiles):
        self.is_rendering = True
        if self.structures_step == -1:
            self.initialize_chunk_variables()
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
        row = TILE_NUMBER // DRAW_RENDER_STEPS * self.draw_step
        for i in range(TILE_NUMBER // DRAW_RENDER_STEPS):
            for j in range(TILE_NUMBER):
                decode(self.tilegrid, self.structuregrid, (row + i, j))
                self.blit(row + i, j, tiles, self.tilegrid)
                if self.structuregrid is not None and is_what(self.structuregrid[row + i][j], ITEM):
                    self.blit(row + i, j, tiles, self.structuregrid)
