from ..setup import graphics_dict


class Tiles:
    def __init__(self):
        self.terrain = [graphics_dict["map"].get_image(0),
                        graphics_dict["map"].get_image(11),
                        graphics_dict["map"].get_image(49)]
        self.structures = []
