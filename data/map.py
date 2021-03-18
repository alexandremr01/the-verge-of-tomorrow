"""
Class supposed to contain enemies that will be rendered at game state
"""

import pygame
import numpy as np
from pygame.locals import K_w, K_a, K_s, K_d, KEYDOWN, KEYUP

from .constants import CHUNK_SIZE, CHUNK_RECT, CHUNK_ARRAY, TOP_RECT, BOTTOM_RECT, LEFT_RECT, RIGHT_RECT
from .wave import Wave
from .components.player import Player
from .chunk import Chunk
from .tile import Tile


class Map:
    def __init__(self):
        self.time = pygame.time.get_ticks()
        self.player = Player()
        self.is_moving = {K_a: False, K_d: False, K_w: False, K_s: False}
        self.wave = Wave(self.time)

        self.terrain_tiles = []
        self.object_tiles = []
        self.map_surface = pygame.Surface(3 * CHUNK_ARRAY)
        self.chunks = {(0, 0): Chunk(np.array([0, 0]), self.gen_seed())}
        self.loaded_chunks = [(0, 0)]
        self.newly_loaded_chunks = [(0, 0)]
        self.unloaded_chunks = False
        self.chunk_position = self.get_chunk_position()
        self.chunk_quadrant = self.get_chunk_quadrant()

    def get_chunk_position(self):
        """
        Returns the current chunk position on the grid e.g. the primary chunk position is (0, 0)
        its right neighbor is (1, 0) and its bottom neighbor is (0, 1).

        :return: current chunk position on the grid.
        :rtype: numpy array
        """
        player_position = self.player.get_position()
        if CHUNK_RECT.collidepoint(player_position):
            return np.array([0, 0])
        return (np.floor((np.abs(player_position) + CHUNK_ARRAY/2) / CHUNK_SIZE) * np.sign(player_position)).astype(int)

    def get_chunk_quadrant(self):
        """
        Returns vector indicating the quadrant the player is standing on i.e. top, botttom, left, right
        or two of them at a time.

        :return: vector indicating which quadrant the player is on\
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

    def gen_seed(self):
        return 0

    def gen_chunk(self, chunk_position, chunk_quadrant):
        """
        Generates and renders chunk given by chunk_position + chun_quadrant

        :param chunk_position: position of the chunk the player is on
        :type chunk_position: numpy array
        :param chunk_quadrant: vector indicating which quadrant the player is on
        :type chunk_quadrant: numpy array
        """
        chunk_position_pos = tuple(chunk_position + chunk_quadrant)
        if self.chunks.get(chunk_position_pos) is not None:
            if self.chunks[chunk_position_pos].tilegrid is not None:
                return
            self.chunks[chunk_position_pos].render()
        else:
            seed = self.gen_seed()
            self.chunks[chunk_position_pos] = Chunk(np.array(chunk_position_pos), seed)
        self.newly_loaded_chunks.append(chunk_position_pos)
        self.loaded_chunks.append(chunk_position_pos)

    def unload_chunks(self, old_chunk_position, new_chunk_position):
        """
        Unloads the chunks which are neighbors to old_chunk_position but aren't to the new_chunk_position.

        :param old_chunk_position: position of the chunk the player was on
        :type old_chunk_position: numpy array
        :param new_chunk_position: position of the chunk the player was on
        :type new_chunk_position: numpy array
        """
        unload_vector = old_chunk_position - new_chunk_position
        unload_vectors = []
        if np.linalg.norm(unload_vector) > 1:
            x = np.array([unload_vector[0], 0])
            y = np.array([0, unload_vector[1]])
            unload_vectors = [unload_vector, x, y, x - y, y - x]
        else:
            flip = np.flip(unload_vector)
            unload_vectors = [unload_vector, unload_vector + flip, unload_vector - flip]
        for vector in unload_vectors:
            unload_position = tuple(old_chunk_position + vector)
            if self.chunks.get(unload_position) is not None:
                self.chunks[unload_position].tilegrid = None
                self.loaded_chunks.remove(unload_position)

    def update_chunks(self):
        """
        Updates the chunks by creating new ones, rendering already created ones and unloading distant ones.
        """
        chunk_position = self.get_chunk_position()
        if np.all(chunk_position == self.chunk_position):
            chunk_quadrant = self.get_chunk_quadrant()
            if np.any(chunk_quadrant != self.chunk_quadrant):
                self.chunk_quadrant = chunk_quadrant
                if np.linalg.norm(chunk_quadrant) != 0:
                    self.gen_chunk(chunk_position, chunk_quadrant)
                    if np.linalg.norm(chunk_quadrant) > 1:
                        self.gen_chunk(chunk_position, np.array([chunk_quadrant[0], 0]))
                        self.gen_chunk(chunk_position, np.array([0, chunk_quadrant[1]]))
        else:
            self.unload_chunks(self.chunk_position, chunk_position)
            self.chunk_position = chunk_position

    def update_positions(self):
        """
        Updates positions of enemies and objects relative to the player.
        """
        walk_vector = np.array([0, 0])
        if self.is_moving[K_a]:
            walk_vector[0] -= self.player.velocity
        if self.is_moving[K_d]:
            walk_vector[0] += self.player.velocity
        if self.is_moving[K_s]:
            walk_vector[1] += self.player.velocity
        if self.is_moving[K_w]:
            walk_vector[1] -= self.player.velocity
        self.player.move(walk_vector[0], walk_vector[1])

    def handle_input(self, events):
        for event in events:
            if event.type == KEYDOWN:
                self.is_moving[event.key] = True
                self.player.update(event.key)
            if event.type == KEYUP:
                self.is_moving[event.key] = False
                self.player.update()

    def update(self):
        """
        Updates positions of enemies and objects relative to the player,
        spawns new enemies and objects,
        despawns out of range ones.
        """
        self.time = pygame.time.get_ticks()
        if self.wave.finished():
            self.wave.new_wave()
        self.update_positions()
        self.update_chunks()
        print(self.get_chunk_quadrant(), self.loaded_chunks)
        self.wave.update_enemies(self.player, self.time)

    def draw(self, screen):
        """
        Draws onto the screen enemies and objects in sight.
        """
        screen.center_on_player(self.player.get_position())
        self.player.draw(screen)

        for enemy in self.wave.enemies:
            if screen.screen_rect.colliderect(enemy.sprite.rect):
                enemy.draw(screen)

        # if self.unloaded_chunks:
        #     # Redraw every loaded chunk
        # elif len(self.newly_loaded_chunks) is not 0:
        #     # Draw newly loaded chunks
        #     self.newly_loaded_chunks = []


