"""
Class supposed to contain enemies that will be rendered at game state
"""

import numpy as np
from .components import player
from .utils import distance
from .constants import MAP_WIDTH, MAP_HEIGHT, CHUNK_SIZE, BLOCK_SIZE, MAX_OBJECT_COUNT, SPAWN_DISTANCE, \
    DESPAWN_DISTANCE, SCREEN_WIDTH, SCREEN_HEIGHT
from .wave import Wave
from pygame import Rect, rect


class Block:
    def __init__(self, position):
        self.position = position
        self.rect = Rect(position[0], position[1], BLOCK_SIZE, BLOCK_SIZE)
        self.terrain = None
        self.object = None

    def update_position(self, position):
        self.position = position
        self.rect = Rect(position[0], position[1], BLOCK_SIZE, BLOCK_SIZE)

    def is_occupied(self):
        return not (self.object is None)


class Chunk:
    def __init__(self, position):
        self.position = position
        self.rect = Rect(position[0], position[1], CHUNK_SIZE, CHUNK_SIZE)
        self.blockgrid = np.array([[Block(np.array([row, column]) * BLOCK_SIZE + position)
                                    for row in range(CHUNK_SIZE / BLOCK_SIZE)]
                                   for column in range(CHUNK_SIZE / BLOCK_SIZE)])
        self.object_count = 0
        self.enemy_count = 0
        self.terrain_type = None  # TODO: Create different terrain types

    def update_position(self, position):
        self.position = position
        self.rect = Rect(position[0], position[1], CHUNK_SIZE, CHUNK_SIZE)


class Map:
    def __init__(self, width=MAP_WIDTH, height=MAP_HEIGHT):
        self.width = width
        self.height = height
        self.wave = Wave()
        self.wave.new_wave()
        self.chunkgrid = np.array([[Chunk(np.array([row, column]) * CHUNK_SIZE)
                                    for row in range(MAP_HEIGHT / CHUNK_SIZE)]
                                   for column in range(MAP_WIDTH / CHUNK_SIZE)])
        self.player_chunk_position = np.array([0, 0])
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
            elif distance(enemy.get_position(), player.get_position()) > self.despawn_distance:  # GET CENTER POSITIONS
                self.wave.notify_despawn()
            else:
                live_enemies.append(enemy)
        self.enemies = live_enemies
        if self.wave.spawns_left():
            self.enemies.append(self.wave.generate_enemy())

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
        # UPDATES POSITIONS OF enemies
        # walk_vector = get_movement_from_player()
        # self.player_chunk_position = self.player_chunk_position + walk_vector
        # for enemy in self.enemies:
        #   enemy.position = enemy.postion + enemy.ai_move()
        # handle_collisions()  # SOMEHOW

    def update_chunkgrid(self):
        """
        Slices chunkgrid and adds new row or column depending on player movement.
        """
        if self.player_chunk_position[0] > CHUNK_SIZE:
            self.player_chunk_position[0] = self.player_chunk_position[0] - CHUNK_SIZE
            for chunk in self.chunkgrid[:][0]:
                self.object_count -= chunk.object_count
            self.chunkgrid = self.chunkgrid[:][1:]
            new_chunks = np.array([[Chunk()] for row in range(MAP_HEIGHT / CHUNK_SIZE)])
            self.chunkgrid = np.concatenate((self.chunkgrid, new_chunks), axis=1)
        if self.player_chunk_position[0] < - CHUNK_SIZE:
            self.player_chunk_position[0] = self.player_chunk_position[0] + CHUNK_SIZE
            for chunk in self.chunkgrid[:][MAP_WIDTH / CHUNK_SIZE]:
                self.object_count -= chunk.object_count
            self.chunkgrid = self.chunkgrid[:][:MAP_WIDTH / CHUNK_SIZE]
            new_chunks = np.array([[Chunk()] for row in range(MAP_HEIGHT / CHUNK_SIZE)])
            self.chunkgrid = np.concatenate((new_chunks, self.chunkgrid), axis=1)
        if self.player_chunk_position[1] > CHUNK_SIZE:
            self.player_chunk_position[1] = self.player_chunk_position[1] - CHUNK_SIZE
            for chunk in self.chunkgrid[0][:]:
                self.object_count -= chunk.object_count
            self.chunkgrid = self.chunkgrid[1:][:]
            new_chunks = np.array([[Chunk() for column in range(MAP_WIDTH / CHUNK_SIZE)]])
            self.chunkgrid = np.concatenate((new_chunks, self.chunkgrid), axis=0)
        if self.player_chunk_position[1] < - CHUNK_SIZE:
            self.player_chunk_position[1] = self.player_chunk_position[1] + CHUNK_SIZE
            for chunk in self.chunkgrid[MAP_HEIGHT / CHUNK_SIZE][:]:
                self.object_count -= chunk.object_count
            self.chunkgrid = self.chunkgrid[:MAP_HEIGHT / CHUNK_SIZE][:]
            new_chunks = np.array([[Chunk() for column in range(MAP_WIDTH / CHUNK_SIZE)]])
            self.chunkgrid = np.concatenate((self.chunkgrid, new_chunks), axis=0)
        self.reset_map_position()

    def reset_map_position(self):
        for chunk_row in range(MAP_HEIGHT / CHUNK_SIZE):
            for chunk_column in range(MAP_WIDTH / CHUNK_SIZE):
                self.chunkgrid[chunk_row][chunk_column].update_position(
                    np.array([chunk_row, chunk_column]) * CHUNK_SIZE)
                for block_row in range(CHUNK_SIZE / BLOCK_SIZE):
                    for block_column in range(CHUNK_SIZE / BLOCK_SIZE):
                        self.chunkgrid[chunk_row][chunk_column].blockgrid[block_row][block_column].update_position(
                            np.array([block_row, block_column]) * BLOCK_SIZE)

    def update(self):
        """
        Updates positions of enemies and objects relative to the player,
        spawns new enemies and objects,
        despawns out of range ones.
        """
        if self.wave.finished():
            self.wave.new_wave()
        self.update_positions()
        self.spawn_objects()
        self.spawn_enemies()
        self.draw()

    def draw(self, surface):
        """
        Draws onto the screen enemies and objects in sight.
        """
        screen_pos = self.player_chunk_position + np.array([MAP_WIDTH - SCREEN_WIDTH, MAP_HEIGHT - SCREEN_HEIGHT])/2
        screen_rect = Rect(screen_pos[0], screen_pos[1], SCREEN_WIDTH, SCREEN_HEIGHT)
        for chunk in self.chunkgrid:
            if screen_rect.colliderect(chunk.rect):
                for block in chunk.blockgrid:
                    if screen_rect.colliderect(block.rect):
                        block.object.draw(surface)
        for enemy in self.enemies:
            if screen_rect.colliderect(enemy.sprite.rect):
                enemy.draw(surface)


