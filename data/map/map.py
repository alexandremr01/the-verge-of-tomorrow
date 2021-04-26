import pygame
import numpy as np
from pygame.locals import K_w, K_a, K_s, K_d, KEYDOWN, KEYUP, K_LSHIFT, K_r, K_q
from random import randint
from opensimplex import OpenSimplex
from data.constants import DAY_WAVE_DURATION, NIGHT_WAVE_DURATION

from data.constants import CHUNK_SIZE, CHUNK_RECT, CHUNK_ARRAY, TOP_RECT, BOTTOM_RECT, LEFT_RECT, RIGHT_RECT, \
    CHUNK_TILE_RATIO, TILE_SIZE
from data.wave import Wave
from data.components.player import Player
from .chunk import Chunk
from .tile import Tiles
from data.utils import get_grid_positions
from data.utils import is_in_rect
from ..setup import graphics_dict
from data.components.item import ItemGenerator

class Map:
    """
    Class responsible for holding, managing and drawing map objects.
    """

    def __init__(self):
        self.time = pygame.time.get_ticks()
        self.player = Player()
        self.player_can_shoot = True
        self.is_moving = {K_a: False, K_d: False, K_w: False, K_s: False}
        self.wave = Wave(self.time)

        self.tiles = Tiles()
        self.generator = OpenSimplex(randint(0, 10000))
        self.chunks = {(0, 0): Chunk(np.array([0, 0]))}
        self.chunks[(0, 0)].render(self.generator, self.tiles)
        self.rendering_chunks = [(0, 0)]
        self.loaded_chunks = []
        self.chunk_position = self.get_chunk_position()
        self.chunk_quadrant = self.get_chunk_quadrant()

    def get_player(self):
        """
        Returns the player object
        """
        return self.player

    def get_chunk_position(self, position=None):
        """
        Returns the current chunk position on the grid e.g. the primary chunk position is [0, 0]
        its right neighbor is [1, 0] and its bottom neighbor is [0, 1].

        :return: current chunk position on the grid
        :rtype: numpy array
        """
        if position is None:
            player_position = self.player.get_position()
        else:
            player_position = position
        if CHUNK_RECT.collidepoint(player_position):
            return np.array([0, 0])
        return (np.floor((np.abs(player_position) + CHUNK_ARRAY / 2) / CHUNK_SIZE) *
                np.sign(player_position)).astype(int)

    def get_chunk_quadrant(self):
        """
        Returns vector indicating the quadrant the player is standing on i.e. top, botttom, left, right
        or two of them at a time.

        :return: vector indicating which quadrant the player is on
        :rtype: numpy array
        """
        dif = self.player.get_position() - CHUNK_SIZE * self.get_chunk_position()
        quadrant = np.array([0, 0, 0, 0])
        quadrant[0] = TOP_RECT.collidepoint(dif)
        if not quadrant[0]:
            quadrant[1] = BOTTOM_RECT.collidepoint(dif)
        quadrant[2] = LEFT_RECT.collidepoint(dif)
        if not quadrant[2]:
            quadrant[3] = RIGHT_RECT.collidepoint(dif)
        return (np.array([quadrant[3] - quadrant[2], quadrant[1] - quadrant[0]])).astype(int)

    def get_tile(self, position=None, getposition=False):
        if position is None:
            player_position = self.player.get_position()
        else:
            player_position = position
        chunk_position = self.get_chunk_position(position)
        position_in_chunk = player_position - (chunk_position * CHUNK_SIZE - CHUNK_ARRAY / 2)
        j, i = position_in_chunk // TILE_SIZE
        i = int(i - i // CHUNK_TILE_RATIO)
        j = int(j - j // CHUNK_TILE_RATIO)
        if getposition:
            return i, j
        if self.chunks[tuple(chunk_position)].structuregrid is not None:
            if self.tiles.is_what(self.chunks[tuple(chunk_position)].structuregrid[i][j], "ITEM"):
                return self.tiles.tilesdict[self.chunks[tuple(chunk_position)].structuregrid[i][j]]
        return self.tiles.tilesdict[self.chunks[tuple(chunk_position)].tilegrid[i][j]]

    def gen_chunks(self, chunk_positions):
        """
        Generates or renders chunks at chunk_positions if not yet loaded.

        :param chunk_positions: the positions at which to generate chunks
        :type chunk_positions: array of tuples
        """
        for chunk_position in chunk_positions:
            if self.chunks.get(chunk_position) is not None:
                if self.chunks[chunk_position].is_rendered():
                    continue
            else:
                self.chunks[chunk_position] = Chunk(np.array(chunk_position))
            self.chunks[chunk_position].render(self.generator, self.tiles)
            self.rendering_chunks.append(chunk_position)

    def unload_chunks(self, chunk_positions):
        """
        Unloads chunks at chunk_positions if already generated and rendered.

        :param chunk_positions: the positions to unload chunks
        :type chunk_positions: array of tuples
        """
        for unload_position in chunk_positions:
            if self.chunks.get(unload_position) is not None:
                if self.chunks[unload_position].is_rendered():
                    self.chunks[unload_position].de_render()
                    self.loaded_chunks.remove(unload_position)

    def update_chunks(self):
        """
        Updates chunks by creating new ones, rendering already created ones and unloading distant ones.
        A chunk is created/rendered when the player moves to a new quadrant which is not [0, 0].
        A chunk is unloaded when the player moves to a new chunk.
        """
        if len(self.rendering_chunks) > 0:
            for position in self.rendering_chunks:
                self.chunks[position].render(self.generator, self.tiles)
                if not self.chunks[position].is_rendering:
                    self.rendering_chunks.remove(position)
                    self.loaded_chunks.append(position)

        chunk_position = self.get_chunk_position()
        if np.all(chunk_position == self.chunk_position):
            chunk_quadrant = self.get_chunk_quadrant()
            if np.any(chunk_quadrant != self.chunk_quadrant):
                self.chunk_quadrant = chunk_quadrant
                if np.linalg.norm(chunk_quadrant) > 0:
                    self.gen_chunks(get_grid_positions(chunk_position, chunk_quadrant,
                                                       np.linalg.norm(chunk_quadrant) > 1))
        else:
            unload_direction = self.chunk_position - chunk_position
            self.unload_chunks(get_grid_positions(self.chunk_position, unload_direction,
                                                  1 + np.linalg.norm(unload_direction) > 1))
            self.chunk_position = chunk_position

    def update_positions(self):
        """
        Updates positions of player and enemies.
        """
        self.handle_collision()
        walk_vector = np.array([0, 0])
        if self.is_moving[K_a]:
            walk_vector[0] -= self.player.get_velocity()
        if self.is_moving[K_d]:
            walk_vector[0] += self.player.get_velocity()
        if self.is_moving[K_s]:
            walk_vector[1] += self.player.get_velocity()
        if self.is_moving[K_w]:
            walk_vector[1] -= self.player.get_velocity()
        new_position = self.player.get_position() + walk_vector
        chunk = self.chunks[tuple(self.get_chunk_position(new_position))]
        if not chunk.is_rendering:
            if self.is_valid_position(new_position):
                self.player.move(walk_vector[0], walk_vector[1])
            if self.get_tile(new_position).item is not None:
                item = self.get_tile(new_position).item()
                if item.is_potion():
                    self.player.bag.set_item(item, self.time)
                else:
                    item.apply_effect(self.player, self.time)
                i, j = self.get_tile(new_position, True)
                chunk.structuregrid[i][j] = chunk.tilegrid[i][j]
                chunk.surface.blit(self.tiles.tilesdict[chunk.tilegrid[i][j]].sprite.get_image(),
                                   np.array([j, i]) * TILE_SIZE)
                chunk.surface_night.blit(self.tiles.tilesdict[chunk.tilegrid[i][j]].sprite_night.get_image(),
                                   np.array([j, i]) * TILE_SIZE)
        else:
            self.player.move(walk_vector[0], walk_vector[1])

    def handle_input(self, events):
        """
        Handles input from keyboard and mouse.
        """
        if self.player_can_shoot:
            left_mouse_button = pygame.mouse.get_pressed()[0]
            if left_mouse_button:
                self.player.shoot(self.time)
        for event in events:
            if event.type == KEYDOWN:
                if event.key == K_q:
                    self.player.bag.use(self.player, self.time)

            if event.type == KEYDOWN:
                if event.key == K_LSHIFT:
                    self.player.set_running(self.time)
                self.is_moving[event.key] = True
                self.player_can_shoot = False
                self.player.update(event.key)
            if event.type == KEYUP:
                if event.key == K_LSHIFT:
                    self.player.stop_running(self.time)
                self.is_moving[event.key] = False
                self.player_can_shoot = True
                self.player.update(self.time)

    def handle_collision(self):
        """
        Handles colisions between map objects.
        """
        for enemy in self.wave.get_enemies():
            self.player.handle_collision(enemy, self.time)
            self.player.get_projectiles().handle_collision(enemy)

    def is_valid_position(self, new_posic):
        """
        Determines whether the new position is occupied
        or not
        """

        collision = self.get_tile(new_posic).collide
        for enemy in self.wave.get_enemies():
            if not enemy.flying:
                collision = collision or is_in_rect(enemy.sprite.rect, new_posic)

        return not collision

    def is_stone(self, pos):
        """
        Determines whether it's an obstacle in the map or not
        """
        return self.get_tile(pos).collide

    def update(self, loading):
        """
        Updates map object.
        """
        self.time = pygame.time.get_ticks()
        self.update_positions()
        self.player.update_state(self.time)
        self.player.update_direction(not self.wave.is_day())
        if not loading and self.wave.finished():
            self.wave.new_wave(self.time)
        self.update_chunks()
        self.wave.update_enemies(self.player, self.time, self.is_valid_position, self.is_stone)

    def draw(self, screen):
        """
        Draws on the screen the player, enemies and objects in sight.
        """
        if self.wave.is_day():
            for position in self.loaded_chunks:
                screen.blit(self.chunks[position].surface, self.chunks[position].topleft)
        else:
            for position in self.loaded_chunks:
                screen.blit(self.chunks[position].surface_night, self.chunks[position].topleft)
        for enemy in self.wave.enemies:
            if screen.screen_rect.colliderect(enemy.sprite.rect):
                enemy.draw(screen)
        screen.center_on_player(self.player.get_position())

        self.player.draw(screen, self.wave.is_day())
        self.wave.draw(screen, self.time)

