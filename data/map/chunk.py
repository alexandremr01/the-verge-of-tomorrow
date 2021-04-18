import pygame
import numpy as np
from data.components.item import ItemGenerator
from data.utils import compare
from data.constants import CHUNK_SIZE, CHUNK_ARRAY, TILE_SIZE, RENDER_STEPS, CHUNK_TILE_RATIO, CHUNK_TILE_RATIO_STEPS


class Chunk:
    def __init__(self, position):
        self.position = position
        self.topleft = position * CHUNK_SIZE - CHUNK_ARRAY / 2
        self.itemgenerator = ItemGenerator()
        self.items = []
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
        self.item_generator = ItemGenerator()

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
        new_load = np.array([[(generator.noise2d((start_position[0] / TILE_SIZE + j) / 3,
                                                 -(start_position[1] / TILE_SIZE + i) / 3) + 1) / 2
                              for j in range(CHUNK_TILE_RATIO)]
                             for i in range(CHUNK_TILE_RATIO_STEPS)])
        if self.terrain_step == 0:
            self.tilegrid = new_load
            self.surface = pygame.Surface(CHUNK_ARRAY)
        else:
            self.tilegrid = np.concatenate((self.tilegrid, new_load), axis=0)

    def check_wall_intersection(self, i, j, tiles):
        if tiles.is_what(self.structuregrid[i][j + 1], "FLOOR"):
            if tiles.is_what(self.structuregrid[i + 1][j], "FLOOR"):
                self.structuregrid[i][j] = tiles.code["WALL_BOTTOM_RIGHT"]
            else:
                self.structuregrid[i][j] = tiles.code["WALL_TOP_RIGHT"]
        else:
            if tiles.is_what(self.structuregrid[i + 1][j], "FLOOR"):
                self.structuregrid[i][j] = tiles.code["WALL_BOTTOM_LEFT"]
            else:
                self.structuregrid[i][j] = tiles.code["WALL_TOP_LEFT"]

    def generate_structure(self, tiles):
        position = 0
        for s in enumerate(self.structures):
            if s[0] == self.structures_step:
                position = s[1]
                break

        horizontal_walls = []
        vertical_walls = []
        floor = []
        corners = []

        for direction, length in self.structures[position]:
            i_direction, j_direction = direction
            width, height = length

            # Set floor
            for x in range(-1, width):
                for y in range(-1, height):
                    i = position[0] + i_direction * y
                    j = position[1] + j_direction * x
                    self.structuregrid[i][j] = tiles.code["CHECKERED_PLAIN"]
                    floor.append([i, j])
                    if [i, j] in horizontal_walls:
                        horizontal_walls.remove([i, j])
                    elif [i, j] in vertical_walls:
                        vertical_walls.remove([i, j])
                    elif [i, j] in corners:
                        corners.remove([i, j])

            # Set left and right walls
            for x in [-2, width]:
                for y in range(-1, height):
                    i = position[0] + i_direction * y
                    j = position[1] + j_direction * x
                    if self.structuregrid[i][j] == tiles.code["WALL_TOP_BOTTOM"]:
                        self.check_wall_intersection(i, j, tiles)
                        corners.append([i, j])
                        horizontal_walls.remove([i, j])
                    elif not tiles.is_what(self.structuregrid[i][j], "FLOOR"):
                        self.structuregrid[i][j] = tiles.code["WALL_LEFT_RIGHT"]
                        vertical_walls.append([i, j])

            # Set top and bottom walls
            for y in [-2, height]:
                for x in range(-1, width):
                    i = position[0] + i_direction * y
                    j = position[1] + j_direction * x
                    if self.structuregrid[i][j] == tiles.code["WALL_LEFT_RIGHT"]:
                        self.check_wall_intersection(i, j, tiles)
                        corners.append([i, j])
                        vertical_walls.remove([i, j])
                    elif not tiles.is_what(self.structuregrid[i][j], "FLOOR"):
                        self.structuregrid[i][j] = tiles.code["WALL_TOP_BOTTOM"]
                        horizontal_walls.append([i, j])

            # Set Corners
            for x in [-2, width]:
                for y in [-2, height]:
                    i = position[0] + i_direction * y
                    j = position[1] + j_direction * x
                    if tiles.is_what(self.structuregrid[i][j], "TERRAIN"):
                        corners.append([i, j])
                        if tiles.is_what(self.structuregrid[i][j + 1], "WALL"):
                            if tiles.is_what(self.structuregrid[i + 1][j], "WALL"):
                                self.structuregrid[i][j] = tiles.code["WALL_TOP_LEFT"]
                            else:
                                self.structuregrid[i][j] = tiles.code["WALL_BOTTOM_LEFT"]
                        else:
                            if tiles.is_what(self.structuregrid[i + 1][j], "WALL"):
                                self.structuregrid[i][j] = tiles.code["WALL_TOP_RIGHT"]
                            else:
                                self.structuregrid[i][j] = tiles.code["WALL_BOTTOM_RIGHT"]

        # Select which walls will be doors
        for i in range(len(vertical_walls)):
            f = vertical_walls[i]
            s = vertical_walls[i + 1]
            if f[1] == s[1]:
                if not tiles.is_what(self.structuregrid[f[0] + 1][f[1]], "CORNER") and not tiles.is_what(
                        self.structuregrid[f[0] - 1][f[1]], "CORNER"):
                    if not tiles.is_what(self.structuregrid[s[0] + 1][s[1]], "CORNER") and not tiles.is_what(
                            self.structuregrid[s[0] - 1][s[1]], "CORNER"):
                        vertical_walls.remove(f)
                        vertical_walls.remove(s)
                        self.structuregrid[f[0]][f[1]] = tiles.code["WALL_BROKEN"]
                        self.structuregrid[s[0]][s[1]] = tiles.code["WALL_BROKEN"]
                        for pos in [f, s]:
                            if tiles.is_what(self.structuregrid[pos[0] + 1][pos[1]], "WALL"):
                                self.structuregrid[pos[0] + 1][pos[1]] = tiles.code["WALL_BOTTOM_CORNER_BROKEN"]
                            else:
                                self.structuregrid[pos[0] - 1][pos[1]] = tiles.code["WALL_TOP_CORNER_BROKEN"]
                        break
        for i in range(len(horizontal_walls)):
            f = horizontal_walls[i]
            s = horizontal_walls[i + 1]
            if f[0] == s[0]:
                if not tiles.is_what(self.structuregrid[f[0]][f[1] + 1], "CORNER") and not tiles.is_what(
                        self.structuregrid[f[0]][f[1] - 1], "CORNER"):
                    if not tiles.is_what(self.structuregrid[s[0]][s[1] + 1], "CORNER") and not tiles.is_what(
                            self.structuregrid[s[0]][s[1] - 1], "CORNER"):
                        horizontal_walls.remove(f)
                        horizontal_walls.remove(s)
                        self.structuregrid[f[0]][f[1]] = tiles.code["WALL_BROKEN"]
                        self.structuregrid[s[0]][s[1]] = tiles.code["WALL_BROKEN"]
                        for pos in [f, s]:
                            if tiles.is_what(self.structuregrid[pos[0]][pos[1] + 1], "WALL"):
                                self.structuregrid[pos[0]][pos[1] + 1] = tiles.code["WALL_RIGHT_CORNER_BROKEN"]
                            else:
                                self.structuregrid[pos[0]][pos[1] - 1] = tiles.code["WALL_LEFT_CORNER_BROKEN"]
                    break

        # Puts shadow on tiles
        for wall_position in vertical_walls:
            if tiles.is_what(self.structuregrid[wall_position[0]][wall_position[1] + 1], "FLOOR"):
                self.structuregrid[wall_position[0]][wall_position[1] + 1] = tiles.code["CHECKERED_SHADOW_LEFT"]
            elif tiles.is_what(self.structuregrid[wall_position[0]][wall_position[1] + 1], "TERRAIN"):
                np.random.seed(self.seed + wall_position[0] + wall_position[1])
                self.structuregrid[wall_position[0]][wall_position[1] + 1] = \
                    np.random.choice([tiles.code["GRASS_SHADOW_LEFT_1"], tiles.code["GRASS_SHADOW_LEFT_2"]])
        for wall_position in horizontal_walls:
            if tiles.is_what(self.structuregrid[wall_position[0] + 1][wall_position[1]], "FLOOR"):
                self.structuregrid[wall_position[0] + 1][wall_position[1]] = tiles.code["CHECKERED_SHADOW_TOP"]
            elif tiles.is_what(self.structuregrid[wall_position[0] + 1][wall_position[1]], "TERRAIN"):
                np.random.seed(self.seed + wall_position[0] + wall_position[1])
                self.structuregrid[wall_position[0] + 1][wall_position[1]] = \
                    np.random.choice([tiles.code["GRASS_SHADOW_TOP_1"], tiles.code["GRASS_SHADOW_TOP_2"]])
        for corner in corners:
            if self.structuregrid[corner[0]][corner[1]] == tiles.code["WALL_TOP_RIGHT"]:
                if not tiles.is_what(self.structuregrid[corner[0]][corner[1] + 1], "TERRAIN"):
                    self.structuregrid[corner[0]][corner[1] + 1] = tiles.code["CHECKERED_SHADOW_LEFT_CORNER"]
                else:
                    self.structuregrid[corner[0]][corner[1] + 1] = tiles.code["GRASS_SHADOW_LEFT_CORNER"]
            if self.structuregrid[corner[0]][corner[1]] == tiles.code["WALL_BOTTOM_LEFT"]:
                if not tiles.is_what(self.structuregrid[corner[0] + 1][corner[1]], "TERRAIN"):
                    self.structuregrid[corner[0] + 1][corner[1]] = tiles.code["CHECKERED_SHADOW_TOP_CORNER"]
                else:
                    self.structuregrid[corner[0] + 1][corner[1]] = tiles.code["GRASS_SHADOW_TOP_CORNER"]
            if self.structuregrid[corner[0]][corner[1]] == tiles.code["WALL_BOTTOM_RIGHT"]:
                if not tiles.is_what(self.structuregrid[corner[0] + 1][corner[1] + 1], "TERRAIN"):
                    self.structuregrid[corner[0] + 1][corner[1]] = tiles.code["CHECKERED_SHADOW_TOP"]
                    self.structuregrid[corner[0]][corner[1] + 1] = tiles.code["CHECKERED_SHADOW_LEFT"]
                    self.structuregrid[corner[0] + 1][corner[1] + 1] = tiles.code["CHECKERED_SHADOW_TOP_LEFT"]
                else:
                    self.structuregrid[corner[0] + 1][corner[1]] = tiles.code["GRASS_SHADOW_TOP_1"]
                    self.structuregrid[corner[0]][corner[1] + 1] = tiles.code["GRASS_SHADOW_LEFT_1"]
                    self.structuregrid[corner[0] + 1][corner[1] + 1] = tiles.code["GRASS_SHADOW_TOP_LEFT"]
            if self.structuregrid[corner[0]][corner[1]] == tiles.code["WALL_TOP_LEFT"]:
                if not tiles.is_what(self.structuregrid[corner[0] + 1][corner[1] + 1], "TERRAIN"):
                    self.structuregrid[corner[0] + 1][corner[1] + 1] = tiles.code["CHECKERED_SHADOW_TOP_LEFT_FULL"]
                else:
                    self.structuregrid[corner[0] + 1][corner[1] + 1] = tiles.code["GRASS_SHADOW_TOP_LEFT_FULL"]

        # Generating items
        np.random.seed(self.seed)
        item_position = floor[np.random.randint(len(floor))]

        item = self.item_generator.generate_item()
        self.structuregrid[item_position[0]][item_position[1]] = tiles.code[item.get_sprite()]  # Should generate random item

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
                self.surface.blit(tiles.tilesdict[self.tilegrid[row + i][j]].sprite.get_image(),
                                  np.array([j, row + i]) * TILE_SIZE)
                if self.structuregrid is not None and tiles.is_what(self.structuregrid[row + i][j], "ITEM"):
                    self.surface.blit(tiles.tilesdict[self.structuregrid[row + i][j]].sprite.get_image(),
                                      np.array([j, row + i]) * TILE_SIZE)

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
        elif (tiles.is_what(self.structuregrid[i][j], "FLOOR") or tiles.is_what(self.structuregrid[i][j], "ITEM"))\
                and not tiles.is_what(self.structuregrid[i][j], "FLOOR_SHADOW"):
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
