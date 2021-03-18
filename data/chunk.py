import pygame
from .constants import CHUNK_SIZE


class Chunk:
    def __init__(self, coordinates, seed):
        self.coordinates = coordinates
        self.rect = pygame.Rect(coordinates[0], coordinates[1], CHUNK_SIZE, CHUNK_SIZE)
        self.seed = seed
        self.tilegrid = self.render()

    def render(self):
        # Using seed renders the tilegrid
        pass

    def draw(self):
        pass
