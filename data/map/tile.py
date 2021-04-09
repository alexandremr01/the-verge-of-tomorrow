from ..setup import graphics_dict
from ..components.base.sprite import Sprite


class Tile:
    """
    Individual tile with name, sprite and walkable flag.
    """

    def __init__(self, sprite, walkable=True):
        self.sprite = sprite
        self.walkable = walkable


class Tiles:
    """
    Class that holds all tiles that could be rendered by the map.
    """

    def __init__(self):
        self.code = {"GRASS_PLAIN": 1,
                     "GRASS_DARKLEAFS_1": 2,
                     "GRASS_DARKLEAFS_2": 3,
                     "GRASS_BRIGHTLEAFS_1": 4,
                     "GRASS_BRIGHTLEAFS_2": 5,
                     "GRASS_BRIGHTLEAFS_3": 6,
                     "GRASS_BRIGHTLEAFS_4": 7,
                     "ROCK": 8,
                     "CHECKERED_BASIC_1": 9,
                     "CHECKERED_BASIC_2": 10,
                     "CHECKERED_BASIC_3": 11,
                     "CHECKERED_GRASS_1": 12,
                     "CHECKERED_GRASS_2": 13,
                     "CHECKERED_GRASS_3": 14,
                     "WALL_LEFT_RIGHT": 15,
                     "WALL_TOP_BOTTOM": 16,
                     "WALL_BOTTOM_RIGHT": 17,
                     "WALL_TOP_RIGHT": 18,
                     "WALL_BOTTOM_LEFT": 19,
                     "WALL_TOP_LEFT": 20,
                     "WALL_PILLAR": 21,
                     "WALL_BROKEN": 22}

        self.sprites = {1: Tile(Sprite((0, 0), graphics_dict["map"].get_image(0, (50, 50)))),
                        2: Tile(Sprite((0, 0), graphics_dict["map"].get_image(16, (50, 50)))),
                        3: Tile(Sprite((0, 0), graphics_dict["map"].get_image(24, (50, 50)))),
                        4: Tile(Sprite((0, 0), graphics_dict["map"].get_image(15, (50, 50)))),
                        5: Tile(Sprite((0, 0), graphics_dict["map"].get_image(31, (50, 50)))),
                        6: Tile(Sprite((0, 0), graphics_dict["map"].get_image(23, (50, 50)))),
                        7: Tile(Sprite((0, 0), graphics_dict["map"].get_image(32, (50, 50)))),
                        8: Tile(Sprite((0, 0), graphics_dict["map"].get_image(13, (50, 50))), False),
                        9: Tile(Sprite((0, 0), graphics_dict["map"].get_image(11, (50, 50)))),
                        10: Tile(Sprite((0, 0), graphics_dict["map"].get_image(4, (50, 50)))),
                        11: Tile(Sprite((0, 0), graphics_dict["map"].get_image(12, (50, 50)))),
                        12: Tile(Sprite((0, 0), graphics_dict["map"].get_image(5, (50, 50)))),
                        13: Tile(Sprite((0, 0), graphics_dict["map"].get_image(6, (50, 50)))),
                        14: Tile(Sprite((0, 0), graphics_dict["map"].get_image(7, (50, 50)))),
                        15: Tile(Sprite((0, 0), graphics_dict["map"].get_image(25, (50, 50))), False),
                        16: Tile(Sprite((0, 0), graphics_dict["map"].get_image(40, (50, 50))), False),
                        17: Tile(Sprite((0, 0), graphics_dict["map"].get_image(33, (50, 50)), None,
                                        (True, False)), False),
                        18: Tile(Sprite((0, 0), graphics_dict["map"].get_image(36, (50, 50))), False),
                        19: Tile(Sprite((0, 0), graphics_dict["map"].get_image(33, (50, 50))), False),
                        20: Tile(Sprite((0, 0), graphics_dict["map"].get_image(36, (50, 50)), None,
                                        (True, False)), False),
                        21: Tile(Sprite((0, 0), graphics_dict["map"].get_image(0, (50, 50))), False),
                        22: Tile(Sprite((0, 0), graphics_dict["map"].get_image(0, (50, 50))))
                        }

    def is_what(self, value, name):
        if name == "TERRAIN":
            return value == 0 or self.code["GRASS_PLAIN"] <= value <= self.code["ROCK"]
        elif name == "STRUCTURE":
            return self.code["CHECKERED_BASIC_1"] <= value <= self.code["WALL_BROKEN"]
        elif name == "FLOOR":
            return self.code["CHECKERED_BASIC_1"] <= value <= self.code["CHECKERED_GRASS_3"]
        elif name == "WALL":
            return self.code["WALL_LEFT_RIGHT"] <= value <= self.code["WALL_TOP_LEFT"]


