"""
Module containing tests in the forms of maps to be
displayed in the play state
"""

import numpy as np
from .constants import SCREEN_WIDTH, SCREEN_HEIGHT
from .components.base.sprite import Sprite
from .wave import Wave
from .setup import graphics_dict

class SpritesMap:
    """
    Tests functionality of the SpriteSheet class
    """
    def __init__(self):
        """
        type spritesheet : SpriteSheet
        """
        self.map = []
        spritesheet = graphics_dict["test_spritesheet"]
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

    def draw(self, screen):
        """
        Draws its collection of sprites
        """
        for tile in self.map:
            screen.blit(tile.get_image(), tile.get_position())

class WaveMap:
    """
    Tests functionality of the Wave class
    """
    def __init__(self):
        self.enemies = []
        self.enemies_count = 0
        self.wave = Wave()
        self.wave.new_wave()

    def update(self):
        """
        Tests enemies AI
        """
        if self.wave.finished():
            self.wave.new_wave()
        if self.wave.spawns_left():
            self.enemies.append(self.wave.generate_enemy((10 + self.enemies_count*50, 100)))
            self.enemies_count += 1

        alive = []
        for enemy in self.enemies:
            enemy.ai_move(np.array([300, 300]))

            if enemy.estimate_velocity() > 0.01:
                alive.append(enemy)
            else:
                self.wave.notify_kill()
        self.enemies.clear()
        for enemy in alive:
            self.enemies.append(enemy)

    def draw(self, screen):
        """
        Draws enemies
        """
        for enemy in self.enemies:
            enemy.draw(screen)
