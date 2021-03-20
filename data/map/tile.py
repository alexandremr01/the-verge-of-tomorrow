from ..setup import graphics_dict
from ..components.base.sprite import Sprite


class Tile:
    """
    Individual tile with name, sprite and walkable flag.
    """
    def __init__(self, name, sprite, walkable=True):
        self.name = name
        self.sprite = sprite
        self.walkable = walkable


class Tiles:
    """
    Class that holds all tiles that could be rendered by the map.
    """
    def __init__(self):
        self.terrain = {0: Tile("DIRT", Sprite((0, 0), graphics_dict["map"].get_image(49, (50, 50)))),
                        1: Tile("GRASS", Sprite((0, 0), graphics_dict["map"].get_image(0, (50, 50)))),
                        2: Tile("CHECKERED", Sprite((0, 0), graphics_dict["map"].get_image(11, (50, 50))))}
        self.structures = []

