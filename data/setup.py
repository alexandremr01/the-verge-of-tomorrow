"""
Module that will load sprites, audios and other resources
"""

from .components.base.sprite import SpriteSheet
from .constants import BASE_GRAPHICS_DIR

graphics_dict = {}

def load_graphics():
    """
    Loads graphics from archives into the code
    """
    test_spritesheet = SpriteSheet(BASE_GRAPHICS_DIR + 'spritesheet-example.png', (16, 16), 128, 160)
    player_graphics = SpriteSheet(BASE_GRAPHICS_DIR + "player.png", (59, 45), 236, 45)
    zombie_graphics = SpriteSheet(BASE_GRAPHICS_DIR + "zombie.png", (45, 45), 90, 45)
    map_graphics = SpriteSheet(BASE_GRAPHICS_DIR + "jawbreaker.png", (8, 8), 64, 72)
    items_graphics = SpriteSheet(BASE_GRAPHICS_DIR + "items.png", (32, 32), 352, 32)
    bullets_graphics = SpriteSheet(BASE_GRAPHICS_DIR + "firebullet.png", (16, 16), 512, 272)
    status_bar_graphics = SpriteSheet(BASE_GRAPHICS_DIR + "status_bar.png", (800, 100), 800, 100)
    graphics_dict["test_spritesheet"] = test_spritesheet
    graphics_dict["test_sprite"] = test_spritesheet.get_image(1)
    graphics_dict["player"] = player_graphics
    graphics_dict["zombie"] = zombie_graphics
    graphics_dict["map"] = map_graphics
    graphics_dict["items"] = items_graphics
    graphics_dict["bullets"] = bullets_graphics
    graphics_dict["status_bar"] = status_bar_graphics