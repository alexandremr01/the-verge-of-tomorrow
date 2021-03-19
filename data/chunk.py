import pygame
from .constants import CHUNK_SIZE


class Chunk:
    def __init__(self, coordinates, seed):
        self.coordinates = coordinates
        self.rect = pygame.Rect(coordinates[0], coordinates[1], CHUNK_SIZE, CHUNK_SIZE)
        self.seed = seed
        self.tilegrid = None
        self.render()

    def render(self):
        self.tilegrid = [0, 1]

    def draw(self, surface, position):
        pass
