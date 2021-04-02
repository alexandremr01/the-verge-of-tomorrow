import pygame
import numpy as np
from pygame.locals import K_w, K_a, K_s, K_d, KEYDOWN, KEYUP, MOUSEBUTTONUP, MOUSEBUTTONDOWN
from random import randint
from opensimplex import OpenSimplex

from data.constants import CHUNK_SIZE, CHUNK_RECT, CHUNK_ARRAY, TOP_RECT, BOTTOM_RECT, LEFT_RECT, RIGHT_RECT
from data.wave import Wave
from data.components.player import Player
from .chunk import Chunk
from .tile import Tiles
from data.utils import get_grid_positions


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

    def get_chunk_position(self):
        """
        Returns the current chunk position on the grid e.g. the primary chunk position is [0, 0]
        its right neighbor is [1, 0] and its bottom neighbor is [0, 1].

        :return: current chunk position on the grid
        :rtype: numpy array
        """
        player_position = self.player.get_position()
        if CHUNK_RECT.collidepoint(player_position):
            return np.array([0, 0])
        return (np.floor((np.abs(player_position) + CHUNK_ARRAY / 2) / CHUNK_SIZE) * np.sign(player_position)).astype(
            int)

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
        """
        Handles input from keyboard and mouse.
        """
        if self.player_can_shoot:
            left_mouse_button = pygame.mouse.get_pressed()[0]
            if left_mouse_button:
                self.player.shoot(self.time)
        for event in events:
            if event.type == KEYDOWN:
                if not any(self.is_moving.values()):
                    self.is_moving[event.key] = True
                    self.player_can_shoot = False
                    self.player.update(event.key)
            if event.type == KEYUP:
                self.is_moving[event.key] = False
                if not any(self.is_moving.values()):
                    self.player_can_shoot = True
                    self.player.update() 

    def handle_collision(self):
        """
        Handles colisions between map objects.
        """
        for zombie in self.wave.get_zombies():
            self.player.handle_collision(zombie, self.time)
            self.player.get_projectiles().handle_collision(zombie)

    def update(self):
        """
        Updates map object.
        """
        self.time = pygame.time.get_ticks()
        self.handle_collision()
        self.player.update_direction()
        if self.wave.finished():
            self.wave.new_wave()
        self.update_positions()
        self.update_chunks()
        self.wave.update_enemies(self.player, self.time)

    def draw(self, screen):
        """
        Draws on the screen the player, enemies and objects in sight.
        """
        for position in self.loaded_chunks:
            screen.blit(self.chunks[position].surface, self.chunks[position].topleft)

        for enemy in self.wave.enemies:
            if screen.screen_rect.colliderect(enemy.sprite.rect):
                enemy.draw(screen)

        screen.center_on_player(self.player.get_position())
        self.player.draw(screen)

