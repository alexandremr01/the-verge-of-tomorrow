"""
Class supposed to contain enemies that will be rendered at game state
"""

import pygame
import numpy as np
from pygame.locals import K_w, K_a, K_s, K_d, KEYDOWN, KEYUP

from .constants import MAP_WIDTH, MAP_HEIGHT, CHUNK_SIZE, BLOCK_SIZE
from .wave import Wave
from .components.player import Player

class Block:
    def __init__(self, position=(-1, -1)):
        self.position = position
        self.rect = pygame.Rect(position[0], position[1], BLOCK_SIZE, BLOCK_SIZE)
        self.terrain = None
        self.object = None

    def update_position(self, position):
        self.position = position
        self.rect = pygame.Rect(position[0], position[1], BLOCK_SIZE, BLOCK_SIZE)

    def is_occupied(self):
        return not (self.object is None)


class Chunk:
    def __init__(self, position=(-1, -1)):
        self.position = position
        self.rect = pygame.Rect(position[0], position[1], CHUNK_SIZE, CHUNK_SIZE)
        self.blockgrid = np.array([[Block(np.array([row, column]) * BLOCK_SIZE + position)
                                    for row in range(CHUNK_SIZE // BLOCK_SIZE)]
                                   for column in range(CHUNK_SIZE // BLOCK_SIZE)])
        self.object_count = 0
        self.enemy_count = 0
        self.terrain_type = None  # TODO: Create different terrain types

    def update_position(self, position):
        self.position = position
        self.rect = pygame.Rect(position[0], position[1], CHUNK_SIZE, CHUNK_SIZE)


class Map:
    def __init__(self):
        self.time = pygame.time.get_ticks()
        self.wave = Wave(self.time)
        self.chunkgrid = np.array([[Chunk(np.array([row, column]) * CHUNK_SIZE)
                                    for row in range(MAP_HEIGHT // CHUNK_SIZE)]
                                   for column in range(MAP_WIDTH // CHUNK_SIZE)])
        self.player_chunk_position = np.array([0, 0])
        self.player = Player()
        self.is_moving = {K_a: False, K_d: False, K_w: False, K_s: False}
        self.object_count = 0

    def spawn_objects(self):
        """
        Computes number of objects in game,
        spawns new objects and
        despawns objects that are out of range.
        """
        # self.update_chunkgrid()
        # if self.object_count < MAX_OBJECT_COUNT:
        #   self.chunkgrid[get_spawn_position()].object = gen_random_object()
        #   self.object_count += 1
        pass

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
        self.player_chunk_position = self.player_chunk_position + walk_vector
        self.update_chunkgrid()

    def update_chunkgrid(self):
        """
        Slices chunkgrid and adds new row or column depending on player movement.
        """
        if self.player_chunk_position[0] > CHUNK_SIZE:
            self.player.move(-CHUNK_SIZE, 0)
            for enemy in self.wave.enemies:
                enemy.move(-CHUNK_SIZE, 0)
            self.player_chunk_position[0] = self.player_chunk_position[0] - CHUNK_SIZE
            for chunk in self.chunkgrid[:, 0]:
                self.object_count -= chunk.object_count
            self.chunkgrid = self.chunkgrid[:, 1:]
            new_chunks = np.array([[Chunk()] for row in range(MAP_HEIGHT // CHUNK_SIZE)])
            self.chunkgrid = np.concatenate((self.chunkgrid, new_chunks), axis=1)
            self.reset_map_position()
        if self.player_chunk_position[0] < - CHUNK_SIZE:
            self.player.move(CHUNK_SIZE, 0)
            for enemy in self.wave.enemies:
                enemy.move(CHUNK_SIZE, 0)
            self.player_chunk_position[0] = self.player_chunk_position[0] + CHUNK_SIZE
            for chunk in self.chunkgrid[:, MAP_WIDTH // CHUNK_SIZE - 1]:
                self.object_count -= chunk.object_count
            self.chunkgrid = self.chunkgrid[:, :MAP_WIDTH // CHUNK_SIZE - 1]
            new_chunks = np.array([[Chunk()] for row in range(MAP_HEIGHT // CHUNK_SIZE)])
            self.chunkgrid = np.concatenate((new_chunks, self.chunkgrid), axis=1)
            self.reset_map_position()
        if self.player_chunk_position[1] > CHUNK_SIZE:
            self.player.move(0, -CHUNK_SIZE)
            for enemy in self.wave.enemies:
                enemy.move(0, -CHUNK_SIZE)
            self.player_chunk_position[1] = self.player_chunk_position[1] - CHUNK_SIZE
            for chunk in self.chunkgrid[0, :]:
                self.object_count -= chunk.object_count
            self.chunkgrid = self.chunkgrid[1:, :]
            new_chunks = np.array([[Chunk() for column in range(MAP_WIDTH // CHUNK_SIZE)]])
            self.chunkgrid = np.concatenate((new_chunks, self.chunkgrid), axis=0)
            self.reset_map_position()
        if self.player_chunk_position[1] < - CHUNK_SIZE:
            self.player.move(0, CHUNK_SIZE)
            for enemy in self.wave.enemies:
                enemy.move(0, CHUNK_SIZE)
            self.player_chunk_position[1] = self.player_chunk_position[1] + CHUNK_SIZE
            for chunk in self.chunkgrid[MAP_HEIGHT // CHUNK_SIZE - 1, :]:
                self.object_count -= chunk.object_count
            self.chunkgrid = self.chunkgrid[:MAP_HEIGHT // CHUNK_SIZE - 1, :]
            new_chunks = np.array([[Chunk() for column in range(MAP_WIDTH // CHUNK_SIZE)]])
            self.chunkgrid = np.concatenate((self.chunkgrid, new_chunks), axis=0)
            self.reset_map_position()

    def reset_map_position(self):
        for chunk_row in range(MAP_HEIGHT // CHUNK_SIZE):
            for chunk_column in range(MAP_WIDTH // CHUNK_SIZE):
                self.chunkgrid[chunk_row][chunk_column].update_position(
                    np.array([chunk_row, chunk_column]) * CHUNK_SIZE)
                for block_row in range(CHUNK_SIZE // BLOCK_SIZE):
                    for block_column in range(CHUNK_SIZE // BLOCK_SIZE):
                        self.chunkgrid[chunk_row][chunk_column].blockgrid[block_row][block_column].update_position(
                            np.array([block_row, block_column]) * BLOCK_SIZE)

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
        self.wave.update_enemies(self.player, self.time)
        self.spawn_objects()

    def draw(self, screen):
        """
        Draws onto the screen enemies and objects in sight.
        """
        screen.center_on_player(self.player.get_position())
        self.player.draw(screen)

        for enemy in self.wave.enemies:
            if screen.screen_rect.colliderect(enemy.sprite.rect):
                enemy.draw(screen)

        # for chunk in self.chunkgrid:
        #     if screen_rect.colliderect(chunk.rect):
        #         for block in chunk.blockgrid:
        #             if screen_rect.colliderect(block.rect):
        #                 block.object.draw(screen)
