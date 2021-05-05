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
            height = randint(seed=direction_seed + 5,
                             low=6,
                             high=TILE_NUMBER / 4 - 1)
            generation_variables.append((direction, (width, height)))
        structures[tuple(position)] = generation_variables
    return structures


def gen_terrain_load(generator, topleft, terrain_step):
    starting_position = (topleft +
                         np.array([0, CHUNK_SIZE // TERRAIN_STEPS * terrain_step])) / TILE_SIZE
    load = np.array([[(generator.noise2d((starting_position[0] + j) / 3,
                                         -(starting_position[1] + i) / 3) + 1) / 2
                      for j in range(TILE_NUMBER)]
                     for i in range(TILE_NUMBER // TERRAIN_STEPS)])
    return load


def get_grid_indexes(position, direction, x_value, y_value):
    return position[0] + direction[0] * y_value, position[1] + direction[1] * x_value


def build_floor(structures_array, structures_info, position, interior_floor, border_floor):
    for direction, length in structures_info[position]:
        width, height = length
        for x in range(-1, width):
            for y in range(-1, height):
                i, j = get_grid_indexes(position, direction, x, y)
                structures_array[i, j] = CHECKERED_PLAIN

                is_border = x == -1 or x == width - 1 or y == -1 or y == height - 1
                in_border = True if (i, j) in border_floor else False
                in_interior = True if (i, j) in interior_floor else False

                if is_border:
                    if not in_border:
                        border_floor.append((i, j))
                    elif in_interior:
                        interior_floor.remove((i, j))
                else:
                    if in_border:
                        border_floor.remove((i, j))
                    elif not in_interior:
                        interior_floor.append((i, j))


def build_walls(structures_array, border_floor, horizontal_walls, vertical_walls, corner_walls):
    for floor_pos in border_floor:
        i, j = floor_pos

        top_neighbor = (i - 1, j)
        bottom_neighbor = (i + 1, j)

        left_neighbor = (i, j - 1)
        right_neighbor = (i, j + 1)

        left_top_neighbor = (i - 1, j - 1)
        left_bottom_neighbor = (i + 1, j - 1)

        right_top_neighbor = (i - 1, j + 1)
        right_bottom_neighbor = (i + 1, j + 1)

        build_side_wall(structures_array, horizontal_walls, top_neighbor, WALL_TOP_BOTTOM)
        build_side_wall(structures_array, horizontal_walls, bottom_neighbor, WALL_TOP_BOTTOM)
        build_side_wall(structures_array, vertical_walls, left_neighbor, WALL_LEFT_RIGHT)
        build_side_wall(structures_array, vertical_walls, right_neighbor, WALL_LEFT_RIGHT)

        build_corner_wall(structures_array, corner_walls, left_top_neighbor, left_neighbor, top_neighbor,
                          WALL_TOP_LEFT, WALL_BOTTOM_RIGHT)
        build_corner_wall(structures_array, corner_walls, left_bottom_neighbor, left_neighbor, bottom_neighbor,
                          WALL_BOTTOM_LEFT, WALL_TOP_RIGHT)
        build_corner_wall(structures_array, corner_walls, right_top_neighbor, right_neighbor, top_neighbor,
                          WALL_TOP_RIGHT, WALL_BOTTOM_LEFT)
        build_corner_wall(structures_array, corner_walls, right_bottom_neighbor, right_neighbor, bottom_neighbor,
                          WALL_BOTTOM_RIGHT, WALL_TOP_LEFT)


def build_side_wall(structures_array, wall_list, side_pos, side_type):
    if is_what(structures_array[side_pos], TERRAIN):
        structures_array[side_pos] = side_type
        wall_list.append(side_pos)


def build_corner_wall(structures_array, corner_walls, corner_pos, adjacent_pos1, adjacent_pos2,
                      incorner_type, outcorner_type):
    if is_what(structures_array[corner_pos], TERRAIN):
        if is_what(structures_array[adjacent_pos1], WALL) \
                and is_what(structures_array[adjacent_pos2], WALL):
            structures_array[corner_pos] = incorner_type
            corner_walls.append(corner_pos)
        elif is_what(structures_array[adjacent_pos1], FLOOR) \
                and is_what(structures_array[adjacent_pos2], FLOOR):
            structures_array[corner_pos] = outcorner_type
            corner_walls.append(corner_pos)


def cast_shadows(seed, structures_array, horizontal_walls, vertical_walls, corner_walls):
    for wall_pos in horizontal_walls:
        shadow_pos = (wall_pos[0] + 1, wall_pos[1])
        cast_side_shadow(seed, structures_array, shadow_pos, CHECKERED_SHADOW_TOP,
                         GRASS_SHADOW_TOP_1, GRASS_SHADOW_TOP_2)

    for wall_pos in vertical_walls:
        shadow_pos = (wall_pos[0], wall_pos[1] + 1)
        cast_side_shadow(seed, structures_array, shadow_pos, CHECKERED_SHADOW_LEFT,
                         GRASS_SHADOW_LEFT_1, GRASS_SHADOW_LEFT_2)

    for wall_pos in corner_walls:
        if is_what(structures_array[wall_pos], WALL_TOP_LEFT):
            shadow_pos = (wall_pos[0] + 1, wall_pos[1] + 1)
            cast_normal_corner_shadow(structures_array, shadow_pos,
                                      CHECKERED_SHADOW_TOP_LEFT_FULL, GRASS_SHADOW_TOP_LEFT_FULL)
        elif is_what(structures_array[wall_pos], WALL_BOTTOM_RIGHT):
            corner_shadow_pos = (wall_pos[0] + 1, wall_pos[1] + 1)
            left_shadow_pos = (wall_pos[0], wall_pos[1] + 1)
            top_shadow_pos = (wall_pos[0] + 1, wall_pos[1])
            cast_exception_corner_shadow(seed, structures_array, corner_shadow_pos, left_shadow_pos, top_shadow_pos,
                                         CHECKERED_SHADOW_TOP_LEFT, GRASS_SHADOW_TOP_LEFT,
                                         CHECKERED_SHADOW_LEFT, GRASS_SHADOW_LEFT_1, GRASS_SHADOW_LEFT_2,
                                         CHECKERED_SHADOW_TOP, GRASS_SHADOW_TOP_1, GRASS_SHADOW_TOP_2)
        elif is_what(structures_array[wall_pos], WALL_TOP_RIGHT):
            shadow_pos = (wall_pos[0], wall_pos[1] + 1)
            cast_normal_corner_shadow(structures_array, shadow_pos,
                                      CHECKERED_SHADOW_LEFT_CORNER, GRASS_SHADOW_LEFT_CORNER)
        elif is_what(structures_array[wall_pos], WALL_BOTTOM_LEFT):
            shadow_pos = (wall_pos[0] + 1, wall_pos[1])
            cast_normal_corner_shadow(structures_array, shadow_pos,
                                      CHECKERED_SHADOW_TOP_CORNER, GRASS_SHADOW_TOP_CORNER)


def cast_side_shadow(seed, structures_array, shadow_pos, floor_shadow_type, terrain_shadow_type1, terrain_shadow_type2):
    if is_what(structures_array[shadow_pos], FLOOR):
        structures_array[shadow_pos] = floor_shadow_type
    else:
        structures_array[shadow_pos] = randchoice(seed + shadow_pos[1],
                                                  [terrain_shadow_type1, terrain_shadow_type2])


def cast_normal_corner_shadow(structures_array, shadow_pos, floor_shadow_type, terrain_shadow_type):
    if is_what(structures_array[shadow_pos], FLOOR):
        structures_array[shadow_pos] = floor_shadow_type
    elif is_what(structures_array[shadow_pos], TERRAIN):
        structures_array[shadow_pos] = terrain_shadow_type


def cast_exception_corner_shadow(seed, structures_array, corner_shadow_pos, left_shadow_pos, top_shadow_pos,
                                 floor_corner_shadow_type, terrain_corner_shadow_type,
                                 floor_left_shadow_type, terrain_left_shadow_type1, terrain_left_shadow_type2,
                                 floor_top_shadow_type, terrain_top_shadow_type1, terrain_top_shadow_type2):
    if is_what(structures_array[corner_shadow_pos], FLOOR):
        structures_array[corner_shadow_pos] = floor_corner_shadow_type
        structures_array[left_shadow_pos] = floor_left_shadow_type
        structures_array[top_shadow_pos] = floor_top_shadow_type
    elif is_what(structures_array[corner_shadow_pos], TERRAIN):
        structures_array[corner_shadow_pos] = terrain_corner_shadow_type
        structures_array[left_shadow_pos] = randchoice(seed + left_shadow_pos[1],
                                                       [terrain_left_shadow_type1, terrain_left_shadow_type2])
        structures_array[top_shadow_pos] = randchoice(seed + top_shadow_pos[0],
                                                      [terrain_top_shadow_type1, terrain_top_shadow_type2])


def generate_items(seed, structures_array, structures_info, position, interior_floor):
    number_of_items = len(structures_info[position])
    indices = randchoice(seed, list(range(len(interior_floor))), size=number_of_items, replace=False)
    item_positions = np.take(interior_floor, indices=indices, axis=0)
    for item_pos in item_positions:
        item = ItemGenerator().generate_item()
        structures_array[tuple(item_pos)] = item.get_sprite()
