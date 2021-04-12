from ..components.item import Skull
from ..setup import graphics_dict
from ..components.base.sprite import Sprite


class Tile:
    """
    Individual tile with name, sprite and walkable flag.
    """

    def __init__(self, sprite, collide=False, item=None):
        self.sprite = sprite
        self.collide = collide
        self.item = item


class Tiles:
    """
    Class that holds all tiles that could be rendered by the map.
    """

    def __init__(self):
        self.code = {"GRASS_PLAIN": 1,

                     "GRASS_SHADOW_TOP_1": 2,
                     "GRASS_SHADOW_TOP_2": 3,
                     "GRASS_SHADOW_TOP_CORNER": 4,
                     "GRASS_SHADOW_LEFT_1": 5,
                     "GRASS_SHADOW_LEFT_2": 6,
                     "GRASS_SHADOW_LEFT_CORNER": 7,
                     "GRASS_SHADOW_TOP_LEFT": 8,

                     "GRASS_DARKLEAFS_1": 9,
                     "GRASS_DARKLEAFS_2": 10,

                     "GRASS_BRIGHTLEAFS_1": 11,
                     "GRASS_BRIGHTLEAFS_2": 12,
                     "GRASS_BRIGHTLEAFS_3": 13,
                     "GRASS_BRIGHTLEAFS_4": 14,

                     "ROCK": 15,

                     "ROAD_HORIZONTAL_PLAIN": 20,
                     "ROAD_HORIZONTAL_TOP": 21,
                     "ROAD_HORIZONTAL_BOTTOM": 22,
                     "ROAD_HORIZONTAL_BROKEN_LEFT": 23,
                     "ROAD_HORIZONTAL_BROKEN_RIGHT": 24,
                     "ROAD_VERTICAL_PLAIN": 25,
                     "ROAD_VERTICAL_RIGHT": 26,
                     "ROAD_VERTICAL_LEFT": 27,
                     "ROAD_VERTICAL_BROKEN_TOP": 28,
                     "ROAD_VERTICAL_BROKEN_BOTTOM": 29,

                     "CHECKERED_PLAIN": 40,

                     "CHECKERED_SHADOW_TOP": 41,
                     "CHECKERED_SHADOW_TOP_CORNER": 42,
                     "CHECKERED_SHADOW_LEFT": 43,
                     "CHECKERED_SHADOW_LEFT_CORNER": 44,
                     "CHECKERED_SHADOW_TOP_LEFT": 45,
                     "CHECKERED_SHADOW_TOP_LEFT_FULL": 46,

                     "CHECKERED_BROKEN_1": 47,
                     "CHECKERED_BROKEN_2": 48,

                     "CHECKERED_GRASS_1": 49,
                     "CHECKERED_GRASS_2": 50,
                     "CHECKERED_GRASS_3": 51,

                     "WALL_LEFT_RIGHT": 60,
                     "WALL_TOP_BOTTOM": 61,

                     "WALL_BOTTOM_RIGHT": 62,
                     "WALL_TOP_RIGHT": 63,
                     "WALL_BOTTOM_LEFT": 64,
                     "WALL_TOP_LEFT": 65,

                     "WALL_TOP_CORNER": 66,
                     "WALL_TOP_CORNER_BROKEN": 67,
                     "WALL_BOTTOM_CORNER": 68,
                     "WALL_BOTTOM_CORNER_BROKEN": 69,
                     "WALL_LEFT_CORNER": 70,
                     "WALL_LEFT_CORNER_BROKEN": 71,
                     "WALL_RIGHT_CORNER": 72,
                     "WALL_RIGHT_CORNER_BROKEN": 73,
                     "WALL_PILLAR": 74,

                     "WALL_BROKEN": 75,
                     "WALL_BROKEN_GRASS": 76,
                     "WALL_BROKEN_FLOOR": 77,

                     "ITEM_SKULL": 90,
                     "ITEM_HEALTH": 91,
                     "ITEM_BLUEPOTION": 92,
                     "ITEM_GREENPOTION": 93,
                     "ITEM_AMMO": 94}

        self.tilesdict = {
            1: Tile(Sprite((0, 0), graphics_dict["map"].get_image(0, (50, 50)))),

            2: Tile(Sprite((0, 0), graphics_dict["map"].get_image(22, (50, 50)), initial_angle=-90)),
            3: Tile(Sprite((0, 0), graphics_dict["map"].get_image(30, (50, 50)), initial_angle=-90)),
            4: Tile(Sprite((0, 0), graphics_dict["map"].get_image(14, (50, 50)), initial_angle=-90, flip=(True, False))),
            5: Tile(Sprite((0, 0), graphics_dict["map"].get_image(22, (50, 50)))),
            6: Tile(Sprite((0, 0), graphics_dict["map"].get_image(30, (50, 50)))),
            7: Tile(Sprite((0, 0), graphics_dict["map"].get_image(14, (50, 50)))),
            8: Tile(Sprite((0, 0), graphics_dict["map"].get_image(38, (50, 50)))),

            9: Tile(Sprite((0, 0), graphics_dict["map"].get_image(16, (50, 50)))),
            10: Tile(Sprite((0, 0), graphics_dict["map"].get_image(24, (50, 50)))),

            11: Tile(Sprite((0, 0), graphics_dict["map"].get_image(31, (50, 50)))),
            12: Tile(Sprite((0, 0), graphics_dict["map"].get_image(15, (50, 50)))),
            13: Tile(Sprite((0, 0), graphics_dict["map"].get_image(23, (50, 50)))),
            14: Tile(Sprite((0, 0), graphics_dict["map"].get_image(32, (50, 50)))),

            15: Tile(Sprite((0, 0), graphics_dict["map"].get_image(13, (50, 50))), collide=True),

            20: Tile(Sprite((0, 0), graphics_dict["map"].get_image(49, (50, 50)))),
            21: Tile(Sprite((0, 0), graphics_dict["map"].get_image(57, (50, 50)))),
            22: Tile(Sprite((0, 0), graphics_dict["map"].get_image(57, (50, 50)), flip=(False, True))),
            23: Tile(Sprite((0, 0), graphics_dict["map"].get_image(51, (50, 50)))),
            24: Tile(Sprite((0, 0), graphics_dict["map"].get_image(51, (50, 50)), flip=(True, False))),
            25: Tile(Sprite((0, 0), graphics_dict["map"].get_image(49, (50, 50)), initial_angle=-90)),
            26: Tile(Sprite((0, 0), graphics_dict["map"].get_image(57, (50, 50)), initial_angle=-90)),
            27: Tile(Sprite((0, 0), graphics_dict["map"].get_image(57, (50, 50)), initial_angle=-90, flip=(True, False))),
            28: Tile(Sprite((0, 0), graphics_dict["map"].get_image(51, (50, 50)), initial_angle=-90)),
            29: Tile(Sprite((0, 0), graphics_dict["map"].get_image(51, (50, 50)), initial_angle=-90, flip=(False, True))),

            40: Tile(Sprite((0, 0), graphics_dict["map"].get_image(11, (50, 50)))),

            41: Tile(Sprite((0, 0), graphics_dict["map"].get_image(26, (50, 50)), initial_angle=-90, flip=(True, False))),
            42: Tile(Sprite((0, 0), graphics_dict["map"].get_image(18, (50, 50)), initial_angle=-90, flip=(True, False))),
            43: Tile(Sprite((0, 0), graphics_dict["map"].get_image(26, (50, 50)))),
            44: Tile(Sprite((0, 0), graphics_dict["map"].get_image(18, (50, 50)))),
            45: Tile(Sprite((0, 0), graphics_dict["map"].get_image(3, (50, 50)))),
            46: Tile(Sprite((0, 0), graphics_dict["map"].get_image(2, (50, 50)))),

            47: Tile(Sprite((0, 0), graphics_dict["map"].get_image(12, (50, 50)))),
            48: Tile(Sprite((0, 0), graphics_dict["map"].get_image(4, (50, 50)))),

            49: Tile(Sprite((0, 0), graphics_dict["map"].get_image(5, (50, 50)))),
            50: Tile(Sprite((0, 0), graphics_dict["map"].get_image(6, (50, 50)))),
            51: Tile(Sprite((0, 0), graphics_dict["map"].get_image(7, (50, 50)))),

            60: Tile(Sprite((0, 0), graphics_dict["map"].get_image(25, (50, 50))), collide=True),
            61: Tile(Sprite((0, 0), graphics_dict["map"].get_image(40, (50, 50))), collide=True),

            62: Tile(Sprite((0, 0), graphics_dict["map"].get_image(33, (50, 50)), flip=(True, False)), collide=True),
            63: Tile(Sprite((0, 0), graphics_dict["map"].get_image(36, (50, 50))), collide=True),
            64: Tile(Sprite((0, 0), graphics_dict["map"].get_image(33, (50, 50))), collide=True),
            65: Tile(Sprite((0, 0), graphics_dict["map"].get_image(36, (50, 50)), flip=(True, False)), collide=True),

            66: Tile(Sprite((0, 0), graphics_dict["map"].get_image(29, (50, 50)), flip=(False, True)), collide=True),
            67: Tile(Sprite((0, 0), graphics_dict["map"].get_image(1, (50, 50))), collide=True),
            68: Tile(Sprite((0, 0), graphics_dict["map"].get_image(21, (50, 50))), collide=True),
            69: Tile(Sprite((0, 0), graphics_dict["map"].get_image(1, (50, 50)), flip=(False, True)), collide=True),
            70: Tile(Sprite((0, 0), graphics_dict["map"].get_image(20, (50, 50))), collide=True),
            71: Tile(Sprite((0, 0), graphics_dict["map"].get_image(25, (50, 50))), collide=True),
            72: Tile(Sprite((0, 0), graphics_dict["map"].get_image(20, (50, 50)), flip=(True, False)), collide=True),
            73: Tile(Sprite((0, 0), graphics_dict["map"].get_image(25, (50, 50)), flip=(True, False)), collide=True),
            74: Tile(Sprite((0, 0), graphics_dict["map"].get_image(37, (50, 50)))),

            75: Tile(Sprite((0, 0), graphics_dict["map"].get_image(9, (50, 50)))),
            76: Tile(Sprite((0, 0), graphics_dict["map"].get_image(8, (50, 50)))),
            77: Tile(Sprite((0, 0), graphics_dict["map"].get_image(10, (50, 50)))),

            90: Tile(Sprite((0, 0), graphics_dict["map"].get_image(37, (50, 50))), item=1),
            91: Tile(Sprite((0, 0), graphics_dict["map"].get_image(37, (50, 50))), item=2),
            92: Tile(Sprite((0, 0), graphics_dict["map"].get_image(37, (50, 50))), item=3),
            93: Tile(Sprite((0, 0), graphics_dict["map"].get_image(37, (50, 50))), item=4),
            94: Tile(Sprite((0, 0), graphics_dict["map"].get_image(37, (50, 50))), item=5)
        }

    def is_what(self, value, name):
        if name == "TERRAIN":
            return value == 0 or self.code["GRASS_PLAIN"] <= value <= self.code["ROCK"]
        elif name == "STRUCTURE":
            return self.code["CHECKERED_PLAIN"] <= value <= self.code["WALL_BROKEN_FLOOR"]
        elif name == "FLOOR":
            return (self.code["CHECKERED_PLAIN"] <= value <= self.code["CHECKERED_GRASS_3"]) or (value == self.code["WALL_BROKEN_FLOOR"])
        elif name == "FLOOR_SHADOW":
            return self.code["CHECKERED_SHADOW_TOP"] <= value <= self.code["CHECKERED_SHADOW_TOP_LEFT_FULL"]
        elif name == "WALL":
            return self.code["WALL_LEFT_RIGHT"] <= value <= self.code["WALL_PILLAR"]
        elif name == "CORNER":
            return self.code["WALL_BOTTOM_RIGHT"] <= value <= self.code["WALL_TOP_LEFT"]
        elif name == "ITEM":
            return self.code["ITEM_SKULL"] <= value <= self.code["ITEM_AMMO"]


