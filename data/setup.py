"""
Module that will load sprites, audios and other
resources
"""

from .components.base.sprite import SpriteSheet
from .constants import BASE_GRAPHICS_DIR

graphics_dict = {}

def load_graphics():
    """
    Loads graphics from archives into the code
    """
    test_spritesheet = SpriteSheet(BASE_GRAPHICS_DIR + 'spritesheet-example.png', 16, 128, 160)
    graphics_dict["test_spritesheet"] = test_spritesheet
    graphics_dict["test_sprite"] = test_spritesheet.get_image(1)
