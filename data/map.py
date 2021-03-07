"""
Class supposed to contain entities that will be rendered at game state
"""

import numpy as np
from .constants import SCREEN_HEIGHT, SCREEN_WIDTH
from .constants import MAP_WIDTH, MAP_HEIGHT, CHUNK_SIZE, MAX_OBJECT_COUNT
from .components.base.sprite import Sprite
from .wave import Wave

class Chunk:
    def __init__(self, position=(-1, -1)):
        self.position = position
        self.entity_count = 0
        self.object = None

    def is_occupied(self):
        return not (self.object is None)


class Map:
    def __init__(self, spawn_parameters, width=MAP_WIDTH, height=MAP_HEIGHT, chunk_size=CHUNK_SIZE):
        self.width = width
        self.height = height
        self.wave = Wave()
        self.wave.new_wave()

        self.chunk_size = CHUNK_SIZE
        self.gridmap = np.array([[Chunk(np.array([row, column]) * CHUNK_SIZE)
                                  for row in range(MAP_HEIGHT / CHUNK_SIZE)]
                                 for column in range(MAP_WIDTH / CHUNK_SIZE)])
        self.chunk_position = np.array([0, 0])
        self.object_count = 0
        self.spawn_distance = spawn_parameters["spawn_distance"]
        self.despawn_distance = spawn_parameters["despawn_distance"]
        self.entities = []

    def spawn_entities(self):
        """
        Computes number of entities in game,
        despawns entities that are either dead or out of range and
        based on wave parameters spawns new entities.
        """

        # r_entity = []
        # index = 0
        # for entity in self.entities:
        #   if entity.health == 0:
        #       self.wave.notify_kill()
        #       r_entity.append(index)
        #   index += 1
        # self.entitites = np.delete(self.entities, r_entity)

        # EITHER THIS OR THAT REMOVES DEAD AND OUT OF RANGE ENTITIES FROM LIST

        # live_entities = []
        # for entity in self.entities:
        #   if entity.health == 0:
        #       self.wave.notify_kill()
        #   elif distance(entity.position, player.position) > self.despawn_distance:
        #       self.wave.notify_despawn()
        #   else:
        #       live_entities.append(entity)
        # self.entities = live_entities

        # IF WAVE NOT CLEARED SPAWNS NEW ENTITY
        # if self.wave.spawns_left():
        #   self.entities.append(self.wave.generate_enemy())
        pass

    def spawn_objects(self):
        """
        Computes number of objects in game,
        spawns new objects and
        despawns objects that are out of range.
        """
        # self.update_gridmap()
        # if self.object_count < MAX_OBJECT_COUNT:
        #   self.gridmap[get_spawn_position()].object = gen_random_object()
        #   self.object_count += 1
        pass

    def update_positions(self):
        """
        Updates positions of entities and objects relative to the player.
        """
        # UPDATES POSITIONS OF ENTITIES
        # walk_vector = get_movement_from_player()
        # self.chunk_position = self.chunk_position + walk_vector
        # for chunk in self.gridmap:
        #   chunk.position = chunk.position - walk_vector
        # for entity in self.entities:
        #   entity.position = entity.postion + entity.ai_move() - walk_vector
        # handle_collisions()  # SOMEHOW

    def update_gridmap(self):
        """
        Slices gridmap and adds new row or column depending on player movement.
        """
        if self.chunk_position[0] > CHUNK_SIZE:
            self.chunk_position[0] = self.chunk_position[0] - CHUNK_SIZE
            for chunk in self.gridmap[:][0]:
                self.object_count -= chunk.is_occupied()
            self.gridmap = self.gridmap[:][1:]
            new_chunks = np.array([[Chunk()] for row in range(MAP_HEIGHT / CHUNK_SIZE)])
            self.gridmap = np.concatenate((self.gridmap, new_chunks), axis=1)
        if self.chunk_position[0] < - CHUNK_SIZE:
            self.chunk_position[0] = self.chunk_position[0] + CHUNK_SIZE
            for chunk in self.gridmap[:][MAP_WIDTH / CHUNK_SIZE]:
                self.object_count -= chunk.is_occupied()
            self.gridmap = self.gridmap[:][:MAP_WIDTH / CHUNK_SIZE]
            new_chunks = np.array([[Chunk()] for row in range(MAP_HEIGHT / CHUNK_SIZE)])
            self.gridmap = np.concatenate((new_chunks, self.gridmap), axis=1)
        if self.chunk_position[1] > CHUNK_SIZE:
            self.chunk_position[1] = self.chunk_position[1] - CHUNK_SIZE
            for chunk in self.gridmap[0][:]:
                self.object_count -= chunk.is_occupied()
            self.gridmap = self.gridmap[1:][:]
            new_chunks = np.array([[Chunk() for column in range(MAP_WIDTH / CHUNK_SIZE)]])
            self.gridmap = np.concatenate((new_chunks, self.gridmap), axis=0)
        if self.chunk_position[1] < - CHUNK_SIZE:
            self.chunk_position[0] = self.chunk_position[0] + CHUNK_SIZE
            for chunk in self.gridmap[MAP_HEIGHT / CHUNK_SIZE][:]:
                self.object_count -= chunk.is_occupied()
            self.gridmap = self.gridmap[:MAP_HEIGHT / CHUNK_SIZE][:]
            new_chunks = np.array([[Chunk() for column in range(MAP_WIDTH / CHUNK_SIZE)]])
            self.gridmap = np.concatenate((self.gridmap, new_chunks), axis=0)
        for row in range(MAP_HEIGHT / CHUNK_SIZE):
            for column in range(MAP_WIDTH / CHUNK_SIZE):
                self.gridmap[row][column].position = np.array([row, column]) * CHUNK_SIZE - self.chunk_position

    def update(self):
        """
        Updates positions of entities and objects relative to the player,
        spawns new entities and objects,
        despawns out of range ones.
        """
        if self.wave.finished():
            self.wave.new_wave()

        self.update_positions()
        self.spawn_entities()
        self.spawn_objects()
        self.draw()

    def draw(self):
        """
        Draws onto the screen entities and objects in sight.
        """
        pass

class RandomMap:
    """
    For testing purposes
    """
    def __init__(self, spritesheet):
        """
        type spritesheet : SpriteSheet
        """
        self.map = []
        num_rows = SCREEN_HEIGHT // spritesheet.get_resolution()
        num_columns = SCREEN_WIDTH // spritesheet.get_resolution()
        tile_num = np.random.randint(spritesheet.get_size(), size=(num_rows, num_columns))
        # tile_num = np.ones((num_rows, num_columns), dtype=int) # one tile
        for i in range(num_rows):
            for j in range(num_columns):
                sprite = Sprite(((i * spritesheet.resolution + (spritesheet.resolution // 2)),
                                  (j * spritesheet.resolution + (spritesheet.resolution // 2))),
                                 spritesheet.get_image(tile_num[i][j], (4, 5)))
                self.map.append(sprite)

    def draw(self, surface):
        """
        Draws its collection of sprites
        """
        for tile in self.map:
            surface.blit(tile.get_image(), tile.get_position())
