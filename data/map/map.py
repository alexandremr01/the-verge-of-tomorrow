import pygame
import numpy as np
from pygame.locals import K_w, K_a, K_s, K_d, KEYDOWN, KEYUP, K_LSHIFT, K_r, K_q
from random import randint
from opensimplex import OpenSimplex
from data.constants import DAY_WAVE_DURATION, NIGHT_WAVE_DURATION, TILE_NUMBER

from data.constants import CHUNK_SIZE, CHUNK_ARRAY, TILE_SIZE
from data.wave import Wave
from data.components.player import Player
from .chunk import Chunk
from .tile import Tiles, ITEM, is_what
from data.utils import get_grid_positions
from data.utils import is_in_rect


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
        self.previous_chunk = self.get_chunk_position()
        self.previous_square = self.get_chunk_square()
        self.turn = DayNightFSM(0)

    def get_player(self):
        """
        Returns the player object
        """
        return self.player

    def get_chunk_position(self, position=None):
        """
        Returns the chunk position corresponding to position or to player's current position
        e.g. the primary chunk position is [0, 0]
        its right neighbor is [1, 0] and its bottom neighbor is [0, 1].

        :param position: position to evaluate
        :type position: numpy array
        :return: chunk position on the grid
        :rtype: numpy array
        """
        if position is None:
            rel_pos = self.player.get_position() + CHUNK_ARRAY / 2
        else:
            rel_pos = position + CHUNK_ARRAY / 2
        return rel_pos // CHUNK_ARRAY

    def get_chunk_square(self, position=None):
        """
        Returns vector pointing to one of the 9 squares of the chunk corresponding to position or
        to player's current position.

        :param position: position to evaluate
        :type position: numpy array
        :return: vector indicating the square in chunk
        :rtype: numpy array
        """
        if position is None:
            rel_pos = self.player.get_position() + CHUNK_ARRAY / 6 - CHUNK_SIZE * self.get_chunk_position()
        else:
            rel_pos = position + CHUNK_ARRAY / 6 - CHUNK_SIZE * self.get_chunk_position()
        return rel_pos // (CHUNK_ARRAY / 3)

    def get_tile_position(self, position=None):
        """
        Returns tile position on chunk's tilegrid corresponding to position or to player's current position.

        :param position: position to evaluate
        :type position: numpy array
        :return: tile position on chunk's tilegrid
        :rtype: tuple
        """
        if position is None:
            rel_pos = self.player.get_position() + CHUNK_ARRAY / 2 - CHUNK_SIZE * self.get_chunk_position(position)
        else:
            rel_pos = position + CHUNK_ARRAY / 2 - CHUNK_SIZE * self.get_chunk_position(position)
        grid_pos = rel_pos // TILE_SIZE - rel_pos // CHUNK_SIZE  # Clamping end of chunk
        j, i = grid_pos.astype(int)
        return i, j

    def get_tile(self, position=None):
        """
        Returns tile on chunk's tilegrid corresponding to position or to player's current position.

        :param position: position to evaluate
        :type position: numpy array
        :return: tile on chunk's tilegrid
        :rtype: Tile object
        """
        tile_position = self.get_tile_position(position)
        current_chunk = self.chunks[tuple(self.get_chunk_position(position))]
        if current_chunk.structuregrid is not None and is_what(current_chunk.structuregrid[tile_position], ITEM):
            return self.tiles.tilesdict[current_chunk.structuregrid[tile_position]]
        return self.tiles.tilesdict[current_chunk.tilegrid[tile_position]]

    def gen_chunks(self, chunk_positions):
        """
        Generates or renders chunks at chunk_positions if not yet loaded.

        :param chunk_positions: the positions at which to generate chunks
        :type chunk_positions: array of tuples
        """
        for position in chunk_positions:
            if self.chunks.get(position) is not None:
                if not self.chunks[position].is_unloaded():
                    continue
            else:
                self.chunks[position] = Chunk(np.array(position))
            self.chunks[position].render(self.generator, self.tiles)
            self.rendering_chunks.append(position)

    def unload_chunks(self, unload_positions):
        """
        Unloads chunks at unload_positions if already generated and rendered.

        :param unload_positions: the positions to unload chunks
        :type unload_positions: array of tuples
        """
        for position in unload_positions:
            if self.chunks.get(position) is not None:
                if not self.chunks[position].is_unloaded():
                    self.chunks[position].de_render()
                    self.loaded_chunks.remove(position)

    def update_chunks(self):
        """
        Updates chunks by creating, rendering and unloading chunks.
        A chunk is created/rendered when the player moves to a not visited square which is not the center one.
        A chunk is unloaded when the chunk is not neighbor to the player's current chunk.
        """
        if self.rendering_chunks:
            for position in self.rendering_chunks:
                self.chunks[position].render(self.generator, self.tiles)
                if self.chunks[position].is_rendered():
                    self.rendering_chunks.remove(position)
                    self.loaded_chunks.append(position)

        current_chunk = self.get_chunk_position()
        if (current_chunk == self.previous_chunk).all():
            current_square = self.get_chunk_square()
            if (current_square != self.previous_square).any():
                if (current_square != [0, 0]).any():
                    self.gen_chunks(get_grid_positions(current_chunk, current_square,
                                                       np.linalg.norm(current_square) > 1))
                self.previous_square = current_square
        else:
            unload_direction = self.previous_chunk - current_chunk
            self.unload_chunks(get_grid_positions(self.previous_chunk, unload_direction,
                                                  1 + np.linalg.norm(unload_direction) > 1))
            self.previous_chunk = current_chunk

    def update_positions(self):
        """
        Updates positions of player and enemies.
        """
        self.handle_collision()

        walk_vector = np.array([0, 0])
        if self.is_moving[K_a]:
            walk_vector[0] -= 1
        if self.is_moving[K_d]:
            walk_vector[0] += 1
        if self.is_moving[K_s]:
            walk_vector[1] += 1
        if self.is_moving[K_w]:
            walk_vector[1] -= 1
        walk_vector = walk_vector * self.player.get_velocity()

        new_position = self.player.get_position() + walk_vector
        new_chunk = self.chunks[tuple(self.get_chunk_position(new_position))]
        if new_chunk.is_rendered():
            if self.is_valid_position(new_position):
                self.player.move(walk_vector[0], walk_vector[1])
            if self.get_tile(new_position).item is not None:
                item = self.get_tile(new_position).item()
                if item.is_potion():
                    self.player.bag.set_item(item, self.time)
                else:
                    item.apply_effect(self.player, self.time)
                i, j = self.get_tile_position(new_position)
                new_chunk.structuregrid[i][j] = new_chunk.tilegrid[i][j]
                new_chunk.surface.blit(self.tiles.tilesdict[new_chunk.tilegrid[i][j]].sprite.get_image(),
                                       np.array([j, i]) * TILE_SIZE)
                new_chunk.surface_night.blit(self.tiles.tilesdict[new_chunk.tilegrid[i][j]].sprite_night.get_image(),
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
        for zombie in self.wave.get_zombies():
            self.player.handle_collision(zombie, self.time)
            self.player.get_projectiles().handle_collision(zombie)

    def is_valid_position(self, new_posic):
        """
        Determines whether the new position is occupied or not.
        """
        collision = self.get_tile(new_posic).collide
        for zombie in self.wave.get_zombies():
            collision = collision or is_in_rect(zombie.sprite.rect, new_posic)
        return not collision

    def update(self):
        """
        Updates map object.
        """
        self.time = pygame.time.get_ticks()
        self.turn.update(self.time)
        self.update_positions()
        self.player.update_state(self.time)
        self.player.update_direction(not self.turn.is_day())
        if self.wave.finished():
            self.wave.new_wave()
        self.update_chunks()
        self.wave.update_enemies(self.player, self.time, lambda pos: not self.get_tile(pos).collide)

    def draw(self, screen):
        """
        Draws on the screen the player, enemies and objects in sight.
        """
        if self.turn.is_day():
            for position in self.loaded_chunks:
                screen.blit(self.chunks[position].surface, self.chunks[position].topleft)
        else:
            for position in self.loaded_chunks:
                screen.blit(self.chunks[position].surface_night, self.chunks[position].topleft)

        for enemy in self.wave.enemies:
            if screen.screen_rect.colliderect(enemy.sprite.rect):
                enemy.draw(screen)
        screen.center_on_player(self.player.get_position())

        self.player.draw(screen, self.turn.is_day())


class DayNightFSM:
    def __init__(self, time):
        self._state = Day(time)

    def update(self, time):
        next_state = self._state.update(time)
        if next_state is not None:
            self._state = next_state

    def is_day(self):
        return type(self._state) == Day


class Day:
    def __init__(self, time):
        self.expiration_time = time + DAY_WAVE_DURATION

    def update(self, time):
        if time > self.expiration_time:
            return Night(time)
        return None


class Night:
    def __init__(self, time):
        self.expiration_time = time + NIGHT_WAVE_DURATION

    def update(self, time):
        if time > self.expiration_time:
            return Day(time)
        return None
