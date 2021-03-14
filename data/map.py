"""
Class supposed to contain enemies that will be rendered at game state
"""
import pygame
import numpy as np
from .components import player
from .utils import distance
from .constants import MAP_WIDTH, MAP_HEIGHT, CHUNK_SIZE, BLOCK_SIZE, MAX_OBJECT_COUNT, SPAWN_DISTANCE, \
    DESPAWN_DISTANCE, SCREEN_WIDTH, SCREEN_HEIGHT
from .wave import Wave
from .components.player import Player
from pygame.locals import *


class Block:
    def __init__(self, position):
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
    def __init__(self, position):
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
    def __init__(self, graphics):
        self.time = pygame.time.get_ticks()
        self.wave = Wave()
        self.wave.new_wave()
        self.chunkgrid = np.array([[Chunk(np.array([row, column]) * CHUNK_SIZE)
                                    for row in range(MAP_HEIGHT // CHUNK_SIZE)]
                                   for column in range(MAP_WIDTH // CHUNK_SIZE)])
        self.player_chunk_position = np.array([0, 0])
        self.player = Player(graphics['player'])
        self.is_moving = {K_a: False, K_d: False, K_w: False, K_s: False}
        self.object_count = 0
        self.spawn_distance = SPAWN_DISTANCE
        self.despawn_distance = DESPAWN_DISTANCE
        self.enemies = []

    def spawn_enemies(self):
        """
        Computes number of enemies in game,
        despawns enemies that are either dead or out of range and
        based on wave parameters spawns new enemies.
        """
        live_enemies = []
        for enemy in self.enemies:
            if enemy.health == 0:
                self.wave.notify_kill()
            elif distance(enemy.get_position(), self.player.get_position()) > self.despawn_distance:
                self.wave.notify_despawn()
            else:
                live_enemies.append(enemy)
        self.enemies = live_enemies
        if self.wave.spawns_left():
            self.enemies.append(self.wave.generate_enemy((800, 800)))  # ARRUMAR

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
        # for enemy in self.enemies:
        #     enemy.position = enemy.position + enemy.ai_move()
        # self.update_chunkgrid()

    def update_chunkgrid(self):
        """
        Slices chunkgrid and adds new row or column depending on player movement.
        """
        if self.player_chunk_position[0] > CHUNK_SIZE:
            self.player.move(-CHUNK_SIZE, 0)
            self.player_chunk_position[0] = self.player_chunk_position[0] - CHUNK_SIZE
            for chunk in self.chunkgrid[:][0]:
                self.object_count -= chunk.object_count
            self.chunkgrid = self.chunkgrid[:][1:]
            new_chunks = np.array([[Chunk()] for row in range(MAP_HEIGHT // CHUNK_SIZE)])
            self.chunkgrid = np.concatenate((self.chunkgrid, new_chunks), axis=1)
        if self.player_chunk_position[0] < - CHUNK_SIZE:
            self.player.move(CHUNK_SIZE, 0)
            self.player_chunk_position[0] = self.player_chunk_position[0] + CHUNK_SIZE
            for chunk in self.chunkgrid[:][MAP_WIDTH // CHUNK_SIZE]:
                self.object_count -= chunk.object_count
            self.chunkgrid = self.chunkgrid[:][:MAP_WIDTH // CHUNK_SIZE]
            new_chunks = np.array([[Chunk()] for row in range(MAP_HEIGHT // CHUNK_SIZE)])
            self.chunkgrid = np.concatenate((new_chunks, self.chunkgrid), axis=1)
        if self.player_chunk_position[1] > CHUNK_SIZE:
            self.player.move(0, -CHUNK_SIZE)
            self.player_chunk_position[1] = self.player_chunk_position[1] - CHUNK_SIZE
            for chunk in self.chunkgrid[0][:]:
                self.object_count -= chunk.object_count
            self.chunkgrid = self.chunkgrid[1:][:]
            new_chunks = np.array([[Chunk() for column in range(MAP_WIDTH // CHUNK_SIZE)]])
            self.chunkgrid = np.concatenate((new_chunks, self.chunkgrid), axis=0)
        if self.player_chunk_position[1] < - CHUNK_SIZE:
            self.player.move(0, CHUNK_SIZE)
            self.player_chunk_position[1] = self.player_chunk_position[1] + CHUNK_SIZE
            for chunk in self.chunkgrid[MAP_HEIGHT // CHUNK_SIZE][:]:
                self.object_count -= chunk.object_count
            self.chunkgrid = self.chunkgrid[:MAP_HEIGHT // CHUNK_SIZE][:]
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
        self.spawn_objects()
        self.spawn_enemies()

    def draw(self, surface):
        """
        Draws onto the screen enemies and objects in sight.
        """
        screen_pos = np.array(self.player.get_position()) - np.array([SCREEN_WIDTH, SCREEN_HEIGHT])/2
        screen_rect = pygame.Rect(screen_pos[0], screen_pos[1], SCREEN_WIDTH, SCREEN_HEIGHT)
        self.player.draw(surface, screen_pos)
        # for chunk in self.chunkgrid:
        #     if screen_rect.colliderect(chunk.rect):
        #         for block in chunk.blockgrid:
        #             if screen_rect.colliderect(block.rect):
        #                 block.object.draw(surface)
        for enemy in self.enemies:
            if screen_rect.colliderect(enemy.sprite.rect):
                enemy.draw(surface, screen_pos)


