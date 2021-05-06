from ..components.item import Skull, Health, BluePotion, GreenPotion, Ammo
from ..setup import graphics_dict
from ..components.base.sprite import Sprite


class Tile:
    """
    Individual tile with sprites, collision flag and item.
    """

    def __init__(self, sprite, sprite_night=None, collide=False, item=None):
        self.sprite = sprite
        self.sprite_night = sprite_night
        self.collide = collide
        self.item = item


class Tiles:
    """
    Class that holds all tiles that could be rendered by the map.
    """

    def __init__(self):
        self.tilesdict = {
            GRASS_PLAIN: Tile(Sprite((0, 0), graphics_dict["map"].get_image(0, (50, 50))),
                              Sprite((0, 0), graphics_dict["map_night"].get_image(0, (50, 50)))),

            GRASS_SHADOW_TOP_1: Tile(Sprite((0, 0), graphics_dict["map"].get_image(1, (50, 50))),
                                     Sprite((0, 0), graphics_dict["map_night"].get_image(1, (50, 50)))),
            GRASS_SHADOW_TOP_2: Tile(Sprite((0, 0), graphics_dict["map"].get_image(2, (50, 50))),
                                     Sprite((0, 0), graphics_dict["map_night"].get_image(2, (50, 50)))),
            GRASS_SHADOW_TOP_CORNER: Tile(Sprite((0, 0), graphics_dict["map"].get_image(3, (50, 50))),
                                          Sprite((0, 0), graphics_dict["map_night"].get_image(3, (50, 50)))),
            GRASS_SHADOW_LEFT_1: Tile(Sprite((0, 0), graphics_dict["map"].get_image(4, (50, 50))),
                                      Sprite((0, 0), graphics_dict["map_night"].get_image(4, (50, 50)))),
            GRASS_SHADOW_LEFT_2: Tile(Sprite((0, 0), graphics_dict["map"].get_image(5, (50, 50))),
                                      Sprite((0, 0), graphics_dict["map_night"].get_image(5, (50, 50)))),
            GRASS_SHADOW_LEFT_CORNER: Tile(Sprite((0, 0), graphics_dict["map"].get_image(6, (50, 50))),
                                           Sprite((0, 0), graphics_dict["map_night"].get_image(6, (50, 50)))),
            GRASS_SHADOW_TOP_LEFT: Tile(Sprite((0, 0), graphics_dict["map"].get_image(7, (50, 50))),
                                        Sprite((0, 0), graphics_dict["map_night"].get_image(7, (50, 50)))),
            GRASS_SHADOW_TOP_LEFT_FULL: Tile(Sprite((0, 0), graphics_dict["map"].get_image(55, (50, 50))),
                                             Sprite((0, 0), graphics_dict["map_night"].get_image(55, (50, 50)))),

            GRASS_DARKLEAFS_1: Tile(Sprite((0, 0), graphics_dict["map"].get_image(8, (50, 50))),
                                    Sprite((0, 0), graphics_dict["map_night"].get_image(8, (50, 50)))),
            GRASS_DARKLEAFS_2: Tile(Sprite((0, 0), graphics_dict["map"].get_image(9, (50, 50))),
                                    Sprite((0, 0), graphics_dict["map_night"].get_image(9, (50, 50)))),

            GRASS_BRIGHTLEAFS_1: Tile(Sprite((0, 0), graphics_dict["map"].get_image(10, (50, 50))),
                                      Sprite((0, 0), graphics_dict["map_night"].get_image(10, (50, 50)))),
            GRASS_BRIGHTLEAFS_2: Tile(Sprite((0, 0), graphics_dict["map"].get_image(11, (50, 50))),
                                      Sprite((0, 0), graphics_dict["map_night"].get_image(11, (50, 50)))),
            GRASS_BRIGHTLEAFS_3: Tile(Sprite((0, 0), graphics_dict["map"].get_image(12, (50, 50))),
                                      Sprite((0, 0), graphics_dict["map_night"].get_image(12, (50, 50)))),
            GRASS_BRIGHTLEAFS_4: Tile(Sprite((0, 0), graphics_dict["map"].get_image(13, (50, 50))),
                                      Sprite((0, 0), graphics_dict["map_night"].get_image(13, (50, 50)))),

            ROCK: Tile(Sprite((0, 0), graphics_dict["map"].get_image(14, (50, 50))),
                       Sprite((0, 0), graphics_dict["map_night"].get_image(14, (50, 50))), collide=True),

            ROAD_HORIZONTAL_PLAIN: Tile(Sprite((0, 0), graphics_dict["map"].get_image(15, (50, 50))),
                                        Sprite((0, 0), graphics_dict["map_night"].get_image(15, (50, 50)))),
            ROAD_HORIZONTAL_TOP: Tile(Sprite((0, 0), graphics_dict["map"].get_image(16, (50, 50))),
                                      Sprite((0, 0), graphics_dict["map_night"].get_image(16, (50, 50)))),
            ROAD_HORIZONTAL_BOTTOM: Tile(Sprite((0, 0), graphics_dict["map"].get_image(17, (50, 50))),
                                         Sprite((0, 0), graphics_dict["map_night"].get_image(17, (50, 50)))),
            ROAD_HORIZONTAL_BROKEN_LEFT: Tile(Sprite((0, 0), graphics_dict["map"].get_image(18, (50, 50))),
                                              Sprite((0, 0), graphics_dict["map_night"].get_image(18, (50, 50)))),
            ROAD_HORIZONTAL_BROKEN_RIGHT: Tile(Sprite((0, 0), graphics_dict["map"].get_image(19, (50, 50))),
                                               Sprite((0, 0), graphics_dict["map_night"].get_image(19, (50, 50)))),
            ROAD_VERTICAL_PLAIN: Tile(Sprite((0, 0), graphics_dict["map"].get_image(20, (50, 50))),
                                      Sprite((0, 0), graphics_dict["map_night"].get_image(20, (50, 50)))),
            ROAD_VERTICAL_RIGHT: Tile(Sprite((0, 0), graphics_dict["map"].get_image(21, (50, 50))),
                                      Sprite((0, 0), graphics_dict["map_night"].get_image(21, (50, 50)))),
            ROAD_VERTICAL_LEFT: Tile(Sprite((0, 0), graphics_dict["map"].get_image(22, (50, 50))),
                                     Sprite((0, 0), graphics_dict["map_night"].get_image(22, (50, 50)))),
            ROAD_VERTICAL_BROKEN_TOP: Tile(Sprite((0, 0), graphics_dict["map"].get_image(23, (50, 50))),
                                           Sprite((0, 0), graphics_dict["map_night"].get_image(23, (50, 50)))),
            ROAD_VERTICAL_BROKEN_BOTTOM: Tile(Sprite((0, 0), graphics_dict["map"].get_image(24, (50, 50))),
                                              Sprite((0, 0), graphics_dict["map_night"].get_image(24, (50, 50)))),

            CHECKERED_PLAIN: Tile(Sprite((0, 0), graphics_dict["map"].get_image(25, (50, 50))),
                                  Sprite((0, 0), graphics_dict["map_night"].get_image(25, (50, 50)))),

            CHECKERED_SHADOW_TOP: Tile(Sprite((0, 0), graphics_dict["map"].get_image(26, (50, 50))),
                                       Sprite((0, 0), graphics_dict["map_night"].get_image(26, (50, 50)))),
            CHECKERED_SHADOW_TOP_CORNER: Tile(Sprite((0, 0), graphics_dict["map"].get_image(27, (50, 50))),
                                              Sprite((0, 0), graphics_dict["map_night"].get_image(27, (50, 50)))),
            CHECKERED_SHADOW_LEFT: Tile(Sprite((0, 0), graphics_dict["map"].get_image(28, (50, 50))),
                                        Sprite((0, 0), graphics_dict["map_night"].get_image(28, (50, 50)))),
            CHECKERED_SHADOW_LEFT_CORNER: Tile(Sprite((0, 0), graphics_dict["map"].get_image(29, (50, 50))),
                                               Sprite((0, 0), graphics_dict["map_night"].get_image(29, (50, 50)))),
            CHECKERED_SHADOW_TOP_LEFT: Tile(Sprite((0, 0), graphics_dict["map"].get_image(30, (50, 50))),
                                            Sprite((0, 0), graphics_dict["map_night"].get_image(30, (50, 50)))),
            CHECKERED_SHADOW_TOP_LEFT_FULL: Tile(Sprite((0, 0), graphics_dict["map"].get_image(31, (50, 50))),
                                                 Sprite((0, 0), graphics_dict["map_night"].get_image(31, (50, 50)))),

            CHECKERED_BROKEN_1: Tile(Sprite((0, 0), graphics_dict["map"].get_image(32, (50, 50))),
                                     Sprite((0, 0), graphics_dict["map_night"].get_image(32, (50, 50)))),
            CHECKERED_BROKEN_2: Tile(Sprite((0, 0), graphics_dict["map"].get_image(33, (50, 50))),
                                     Sprite((0, 0), graphics_dict["map_night"].get_image(33, (50, 50)))),

            CHECKERED_GRASS_1: Tile(Sprite((0, 0), graphics_dict["map"].get_image(34, (50, 50))),
                                    Sprite((0, 0), graphics_dict["map_night"].get_image(34, (50, 50)))),
            CHECKERED_GRASS_2: Tile(Sprite((0, 0), graphics_dict["map"].get_image(35, (50, 50))),
                                    Sprite((0, 0), graphics_dict["map_night"].get_image(35, (50, 50)))),
            CHECKERED_GRASS_3: Tile(Sprite((0, 0), graphics_dict["map"].get_image(36, (50, 50))),
                                    Sprite((0, 0), graphics_dict["map_night"].get_image(36, (50, 50)))),

            WALL_LEFT_RIGHT: Tile(Sprite((0, 0), graphics_dict["map"].get_image(37, (50, 50))),
                                  Sprite((0, 0), graphics_dict["map_night"].get_image(37, (50, 50))), collide=True),
            WALL_TOP_BOTTOM: Tile(Sprite((0, 0), graphics_dict["map"].get_image(38, (50, 50))),
                                  Sprite((0, 0), graphics_dict["map_night"].get_image(38, (50, 50))), collide=True),

            WALL_BOTTOM_RIGHT: Tile(Sprite((0, 0), graphics_dict["map"].get_image(39, (50, 50))),
                                    Sprite((0, 0), graphics_dict["map_night"].get_image(39, (50, 50))), collide=True),
            WALL_TOP_RIGHT: Tile(Sprite((0, 0), graphics_dict["map"].get_image(40, (50, 50))),
                                 Sprite((0, 0), graphics_dict["map_night"].get_image(40, (50, 50))), collide=True),
            WALL_BOTTOM_LEFT: Tile(Sprite((0, 0), graphics_dict["map"].get_image(41, (50, 50))),
                                   Sprite((0, 0), graphics_dict["map_night"].get_image(41, (50, 50))), collide=True),
            WALL_TOP_LEFT: Tile(Sprite((0, 0), graphics_dict["map"].get_image(42, (50, 50))),
                                Sprite((0, 0), graphics_dict["map_night"].get_image(42, (50, 50))), collide=True),

            WALL_TOP_CORNER: Tile(Sprite((0, 0), graphics_dict["map"].get_image(43, (50, 50))),
                                  Sprite((0, 0), graphics_dict["map_night"].get_image(43, (50, 50))), collide=True),
            WALL_TOP_CORNER_BROKEN: Tile(Sprite((0, 0), graphics_dict["map"].get_image(44, (50, 50))),
                                         Sprite((0, 0), graphics_dict["map_night"].get_image(44, (50, 50))),
                                         collide=True),
            WALL_BOTTOM_CORNER: Tile(Sprite((0, 0), graphics_dict["map"].get_image(45, (50, 50))),
                                     Sprite((0, 0), graphics_dict["map_night"].get_image(45, (50, 50))), collide=True),
            WALL_BOTTOM_CORNER_BROKEN: Tile(Sprite((0, 0), graphics_dict["map"].get_image(46, (50, 50))),
                                            Sprite((0, 0), graphics_dict["map_night"].get_image(46, (50, 50))),
                                            collide=True),
            WALL_LEFT_CORNER: Tile(Sprite((0, 0), graphics_dict["map"].get_image(47, (50, 50))),
                                   Sprite((0, 0), graphics_dict["map_night"].get_image(47, (50, 50))), collide=True),
            WALL_LEFT_CORNER_BROKEN: Tile(Sprite((0, 0), graphics_dict["map"].get_image(48, (50, 50))),
                                          Sprite((0, 0), graphics_dict["map_night"].get_image(48, (50, 50))),
                                          collide=True),
            WALL_RIGHT_CORNER: Tile(Sprite((0, 0), graphics_dict["map"].get_image(49, (50, 50))),
                                    Sprite((0, 0), graphics_dict["map_night"].get_image(49, (50, 50))), collide=True),
            WALL_RIGHT_CORNER_BROKEN: Tile(Sprite((0, 0), graphics_dict["map"].get_image(50, (50, 50))),
                                           Sprite((0, 0), graphics_dict["map_night"].get_image(50, (50, 50))),
                                           collide=True),
            WALL_PILLAR: Tile(Sprite((0, 0), graphics_dict["map"].get_image(51, (50, 50))),
                              Sprite((0, 0), graphics_dict["map_night"].get_image(51, (50, 50)))),

            WALL_BROKEN: Tile(Sprite((0, 0), graphics_dict["map"].get_image(52, (50, 50))),
                              Sprite((0, 0), graphics_dict["map_night"].get_image(52, (50, 50)))),
            WALL_BROKEN_GRASS: Tile(Sprite((0, 0), graphics_dict["map"].get_image(53, (50, 50))),
                                    Sprite((0, 0), graphics_dict["map_night"].get_image(53, (50, 50)))),
            WALL_BROKEN_FLOOR: Tile(Sprite((0, 0), graphics_dict["map"].get_image(54, (50, 50))),
                                    Sprite((0, 0), graphics_dict["map_night"].get_image(54, (50, 50)))),

            ITEM_SKULL: Tile(Sprite((0, 0), graphics_dict["items"].get_image(3, (50, 50)).convert_alpha()),
                             Sprite((0, 0), graphics_dict["items"].get_image(3, (50, 50)).convert_alpha()), item=Skull),
            ITEM_HEALTH: Tile(Sprite((0, 0), graphics_dict["items"].get_image(2, (50, 50)).convert_alpha()),
                              Sprite((0, 0), graphics_dict["items"].get_image(2, (50, 50)).convert_alpha()),
                              item=Health),
            ITEM_BLUEPOTION: Tile(Sprite((0, 0), graphics_dict["items"].get_image(0, (50, 50)).convert_alpha()),
                                  Sprite((0, 0), graphics_dict["items"].get_image(0, (50, 50)).convert_alpha()),
                                  item=BluePotion),
            ITEM_GREENPOTION: Tile(Sprite((0, 0), graphics_dict["items"].get_image(1, (50, 50)).convert_alpha()),
                                   Sprite((0, 0), graphics_dict["items"].get_image(1, (50, 50)).convert_alpha()),
                                   item=GreenPotion),
            ITEM_AMMO: Tile(Sprite((0, 0), graphics_dict["items"].get_image(10, (50, 50)).convert_alpha()),
                            Sprite((0, 0), graphics_dict["items"].get_image(10, (50, 50)).convert_alpha()), item=Ammo)
        }


def is_what(value, tile_type):
    if tile_type == TERRAIN:
        return value == 0 or GRASS_PLAIN <= value <= ROCK
    elif tile_type == STRUCTURE:
        return CHECKERED_PLAIN <= value <= WALL_BROKEN_FLOOR
    elif tile_type == FLOOR:
        return (CHECKERED_PLAIN <= value <= CHECKERED_GRASS_3) or (value == WALL_BROKEN_FLOOR)
    elif tile_type == FLOOR_SHADOW:
        return CHECKERED_SHADOW_TOP <= value <= CHECKERED_SHADOW_TOP_LEFT_FULL
    elif tile_type == GRASS_SHADOW:
        return GRASS_SHADOW_TOP_1 <= value <= GRASS_SHADOW_TOP_LEFT_FULL
    elif tile_type == WALL:
        return WALL_LEFT_RIGHT <= value <= WALL_PILLAR
    elif tile_type == CORNER:
        return WALL_BOTTOM_RIGHT <= value <= WALL_TOP_LEFT
    elif tile_type == ITEM:
        return ITEM_SKULL <= value <= ITEM_AMMO
    else:
        return value == tile_type


TERRAIN = -1
STRUCTURE = -2
FLOOR = -3
FLOOR_SHADOW = -4
GRASS_SHADOW = -5
WALL = -6
CORNER = -7
ITEM = -8

GRASS_PLAIN = 1

GRASS_SHADOW_TOP_1 = 2
GRASS_SHADOW_TOP_2 = 3
GRASS_SHADOW_TOP_CORNER = 4
GRASS_SHADOW_LEFT_1 = 5
GRASS_SHADOW_LEFT_2 = 6
GRASS_SHADOW_LEFT_CORNER = 7
GRASS_SHADOW_TOP_LEFT = 8
GRASS_SHADOW_TOP_LEFT_FULL = 9

GRASS_DARKLEAFS_1 = 10
GRASS_DARKLEAFS_2 = 11

GRASS_BRIGHTLEAFS_1 = 12
GRASS_BRIGHTLEAFS_2 = 13
GRASS_BRIGHTLEAFS_3 = 14
GRASS_BRIGHTLEAFS_4 = 15

ROCK = 16

ROAD_HORIZONTAL_PLAIN = 20
ROAD_HORIZONTAL_TOP = 21
ROAD_HORIZONTAL_BOTTOM = 22
ROAD_HORIZONTAL_BROKEN_LEFT = 23
ROAD_HORIZONTAL_BROKEN_RIGHT = 24
ROAD_VERTICAL_PLAIN = 25
ROAD_VERTICAL_RIGHT = 26
ROAD_VERTICAL_LEFT = 27
ROAD_VERTICAL_BROKEN_TOP = 28
ROAD_VERTICAL_BROKEN_BOTTOM = 29

CHECKERED_PLAIN = 40

CHECKERED_SHADOW_TOP = 41
CHECKERED_SHADOW_TOP_CORNER = 42
CHECKERED_SHADOW_LEFT = 43
CHECKERED_SHADOW_LEFT_CORNER = 44
CHECKERED_SHADOW_TOP_LEFT = 45
CHECKERED_SHADOW_TOP_LEFT_FULL = 46

CHECKERED_BROKEN_1 = 47
CHECKERED_BROKEN_2 = 48

CHECKERED_GRASS_1 = 49
CHECKERED_GRASS_2 = 50
CHECKERED_GRASS_3 = 51

WALL_LEFT_RIGHT = 60
WALL_TOP_BOTTOM = 61

WALL_BOTTOM_RIGHT = 62
WALL_TOP_RIGHT = 63
WALL_BOTTOM_LEFT = 64
WALL_TOP_LEFT = 65

WALL_TOP_CORNER = 66
WALL_TOP_CORNER_BROKEN = 67
WALL_BOTTOM_CORNER = 68
WALL_BOTTOM_CORNER_BROKEN = 69
WALL_LEFT_CORNER = 70
WALL_LEFT_CORNER_BROKEN = 71
WALL_RIGHT_CORNER = 72
WALL_RIGHT_CORNER_BROKEN = 73
WALL_PILLAR = 74

WALL_BROKEN = 75
WALL_BROKEN_GRASS = 76
WALL_BROKEN_FLOOR = 77

ITEM_SKULL = 90
ITEM_HEALTH = 91
ITEM_BLUEPOTION = 92
ITEM_GREENPOTION = 93
ITEM_AMMO = 94
