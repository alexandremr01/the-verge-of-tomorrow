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
        self.terrain = {0: Tile("GRASS_PLAIN",
                                Sprite((0, 0), graphics_dict["map"].get_image(0, (50, 50)))),
                        1: Tile("GRASS_DARKLEAFS_1",
                                Sprite((0, 0), graphics_dict["map"].get_image(16, (50, 50)))),
                        2: Tile("GRASS_DARKLEAFS_2",
                                Sprite((0, 0), graphics_dict["map"].get_image(24, (50, 50)))),
                        3: Tile("GRASS_BRIGHTLEAFS_1",
                                Sprite((0, 0), graphics_dict["map"].get_image(15, (50, 50)))),
                        4: Tile("GRASS_BRIGHTLEAFS_2",
                                Sprite((0, 0), graphics_dict["map"].get_image(31, (50, 50)))),
                        5: Tile("GRASS_BRIGHTLEAFS_3",
                                Sprite((0, 0), graphics_dict["map"].get_image(23, (50, 50)))),
                        6: Tile("GRASS_BRIGHTLEAFS_4",
                                Sprite((0, 0), graphics_dict["map"].get_image(32, (50, 50)))),
                        7: Tile("ROCK",
                                Sprite((0, 0), graphics_dict["map"].get_image(13, (50, 50))), False)}
        self.structures = {-1: Tile("CHECKERED_BASIC_1",
                                    Sprite((0, 0), graphics_dict["map"].get_image(11, (50, 50)))),
                           -2: Tile("CHECKERED_BASIC_2",
                                    Sprite((0, 0), graphics_dict["map"].get_image(4, (50, 50)))),
                           -3: Tile("CHECKERED_BASIC_3",
                                    Sprite((0, 0), graphics_dict["map"].get_image(12, (50, 50)))),
                           -4: Tile("CHECKERED_GRASS_1",
                                    Sprite((0, 0), graphics_dict["map"].get_image(5, (50, 50)))),
                           -5: Tile("CHECKERED_GRASS_2",
                                    Sprite((0, 0), graphics_dict["map"].get_image(6, (50, 50)))),
                           -6: Tile("CHECKERED_GRASS_3",
                                    Sprite((0, 0), graphics_dict["map"].get_image(7, (50, 50)))),
                           -7: Tile("WALL_LEFT_RIGHT",
                                    Sprite((0, 0), graphics_dict["map"].get_image(25, (50, 50))), False),
                           -8: Tile("WALL_TOP_BOTTOM",
                                    Sprite((0, 0), graphics_dict["map"].get_image(40, (50, 50))), False),
                           -9: Tile("WALL_BOTTOM_RIGHT",
                                    Sprite((0, 0), graphics_dict["map"].get_image(33, (50, 50)), None, (True, False)), False),
                           -10: Tile("WALL_TOP_RIGHT",
                                     Sprite((0, 0), graphics_dict["map"].get_image(36, (50, 50))), False),
                           -11: Tile("WALL_BOTTOM_LEFT",
                                     Sprite((0, 0), graphics_dict["map"].get_image(33, (50, 50))), False),
                           -12: Tile("WALL_TOP_LEFT",
                                     Sprite((0, 0), graphics_dict["map"].get_image(36, (50, 50)), None, (True, False)), False),
                           -13: Tile("WALL_PILLAR",
                                     Sprite((0, 0), graphics_dict["map"].get_image(0, (50, 50))), False),
                           -14: Tile("WALL_BROKEN",
                                     Sprite((0, 0), graphics_dict["map"].get_image(0, (50, 50))))}
