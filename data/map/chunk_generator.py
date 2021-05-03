import pygame
import numpy as np
from data.components.item import ItemGenerator
from data.utils import compare
from data.constants import CHUNK_SIZE, CHUNK_ARRAY, TILE_SIZE, RENDER_STEPS, TILE_NUMBER
from data.map.tile import *

TERRAIN_STEPS = 8

STRUCTURES_SEED = {(TILE_NUMBER * 1 // 4, TILE_NUMBER * 1 // 4): 1, (TILE_NUMBER * 3 // 4, TILE_NUMBER * 3 // 4): 2,
                   (TILE_NUMBER * 1 // 4, TILE_NUMBER * 3 // 4): 3, (TILE_NUMBER * 3 // 4, TILE_NUMBER * 1 // 4): 4}
STRUCTURES = [*STRUCTURES_SEED]
DIRECTIONS_SEED = {(1, 1): 11, (-1, 1): 12,
                   (-1, -1): 13, (1, -1): 14}
DIRECTIONS = [*DIRECTIONS_SEED]


def randchoice(seed, array, size=None, replace=True, p=None):
    np.random.seed(seed)
    return np.random.choice(a=array, size=size, replace=replace, p=p)


def randint(seed, low, high=None, size=None, dtype=int):
    np.random.seed(seed)
    return np.random.randint(low=low, high=high, size=size, dtype=dtype)


def gen_structure_info(seed, structures_number):
    structure_spawns = np.take(a=STRUCTURES,
                               indices=randchoice(seed=seed,
                                                  array=[0, 1, 2, 3],
                                                  size=structures_number,
                                                  replace=False),
                               axis=0)
    structures = {}
    for position in structure_spawns:
        structure_seed = seed + STRUCTURES_SEED[tuple(position)]
        directions_number = randchoice(seed=structure_seed,
                                       array=[1, 2, 3, 4],
                                       p=[0.35, 0.35, 0.2, 0.1])
        build_directions = np.take(a=DIRECTIONS,
                                   indices=randchoice(seed=structure_seed,
                                                      array=[0, 1, 2, 3],
                                                      size=directions_number,
                                                      replace=False),
                                   axis=0)
        generation_variables = []
        for direction in build_directions:
            direction_seed = structure_seed + DIRECTIONS_SEED[tuple(direction)]
            width = randint(seed=direction_seed,
                            low=6,
                            high=TILE_NUMBER / 4 - 1)
            height = randint(seed=direction_seed + 1,
                             low=6,
                             high=TILE_NUMBER / 4 - 1)
            generation_variables.append((direction, (width, height)))
        structures[tuple(position)] = generation_variables
    return structures


def gen_terrain_load(generator, starting_position):
    load = np.array([[(generator.noise2d((starting_position[0] + j) / 3,
                                         -(starting_position[1] + i) / 3) + 1) / 2
                      for j in range(TILE_NUMBER)]
                     for i in range(TILE_NUMBER // TERRAIN_STEPS)])
    return load


def get_grid_indexes(position, direction, x_value, y_value):
    return position[0] + direction[0] * y_value, position[1] + direction[1] * x_value


def build_floor(structures_array, structures_info, position):
    horizontal = []
    vertical = []
    extreme_floor = []
    for directions in structures_info[position]:
        for direction, length in directions:s
            width, height = length
            for x in range(-1, width):
                for y in range(-1, height):
                    i, j = get_grid_indexes(position, direction, x, y)
                    if x == -1 or x == width - 1 or y == -1 or y == height - 1:
                        extreme_floor.append((i, j))
                    structures_array[i, j] = CHECKERED_PLAIN
            for x in range(-2, width + 1):
                for y in [-1, height]:
                    i, j = get_grid_indexes(position, direction, x, y)
                    structures_array[i, j] = WALL
                    horizontal.append((i, j))
            for x in range(-2, height + 1):
                for y in [-1, width]:
                    i, j = get_grid_indexes(position, direction, x, y)
                    vertical.append((i, j))


def get_floor_list(lists, position, direction, width, height):
    pass


def get_horizontal_walls_list(lists, ):
    pass


def get_vertical_walls_list():
    pass


def decode(value):
    pass


class ChunkGen:
    def __init__(self):
        self.tilegrid = None
        self.structuregrid = None
        self.structures = None

    def gen_structure_info(self):
        pass

    def gen_structure(self):
        pass

    def decode(self):
        pass
