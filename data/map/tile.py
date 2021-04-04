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
        self.terrain = {0: Tile("GRASS_PLAIN", Sprite((0, 0), graphics_dict["map"].get_image(0, (50, 50)))),
                        1: Tile("GRASS_DARKLEAFS_1", Sprite((0, 0), graphics_dict["map"].get_image(16, (50, 50)))),
                        2: Tile("GRASS_DARKLEAFS_2", Sprite((0, 0), graphics_dict["map"].get_image(24, (50, 50)))),
                        3: Tile("GRASS_BRIGHTLEAFS_1", Sprite((0, 0), graphics_dict["map"].get_image(15, (50, 50)))),
                        4: Tile("GRASS_BRIGHTLEAFS_2", Sprite((0, 0), graphics_dict["map"].get_image(31, (50, 50)))),
                        5: Tile("GRASS_BRIGHTLEAFS_3", Sprite((0, 0), graphics_dict["map"].get_image(23, (50, 50)))),
                        6: Tile("GRASS_BRIGHTLEAFS_4", Sprite((0, 0), graphics_dict["map"].get_image(32, (50, 50)))),
                        7: Tile("ROCK", Sprite((0, 0), graphics_dict["map"].get_image(13, (50, 50))))}
        self.structures = {0: Tile("CHECKERED_BASIC_1", Sprite((0, 0), graphics_dict["map"].get_image(11, (50, 50)))),
                           1: Tile("CHECKERED_BASIC_2", Sprite((0, 0), graphics_dict["map"].get_image(4, (50, 50)))),
                           2: Tile("CHECKERED_BASIC_3", Sprite((0, 0), graphics_dict["map"].get_image(12, (50, 50)))),
                           3: Tile("WALL_LEFT_RIGHT", Sprite((0, 0), graphics_dict["map"].get_image(25, (50, 50)))),
                           4: Tile("WALL_TOP_BOTTOM", Sprite((0, 0), graphics_dict["map"].get_image(25, (50, 50))), 90),
                           5: Tile("WALL_LEFT_TOP", Sprite((0, 0), graphics_dict["map"].get_image(33, (50, 50))), -90),
                           6: Tile("WALL_LEFT_BOTTOM", Sprite((0, 0), graphics_dict["map"].get_image(33, (50, 50)))),
                           7: Tile("WALL_RIGHT_TOP", Sprite((0, 0), graphics_dict["map"].get_image(25, (50, 50))), -180),
                           8: Tile("WALL_RIGHT_BOTTOM", Sprite((0, 0), graphics_dict["map"].get_image(25, (50, 50))), 90),
                           9: Tile("WALL_PILLAR", Sprite((0, 0), graphics_dict["map"].get_image(0, (50, 50)))),
                           10: Tile("WALL_BROKEN", Sprite((0, 0), graphics_dict["map"].get_image(0, (50, 50))))}
