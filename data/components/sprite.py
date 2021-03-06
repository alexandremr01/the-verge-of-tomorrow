"""
Contains a spritesheet loader and the base class for a sprite
"""

import pygame

class Sprite(pygame.sprite.Sprite):
    """
    Base class for game's sprite
    """
    def __init__(self, initial_center, spritesheet):
        """
        param spritesheet : Sprite's graphics
        type spritesheet : pygame.Surface
        param initial_center : sprite's initial center position
        type initial_center : two-dimensional tuple
        """
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface(spritesheet.get_rect().size).convert_alpha()
        self.image.blit(spritesheet, (0, 0), spritesheet.get_rect())
        self.rect = self.image.get_rect().move(initial_center[0] - self.image.get_rect().width / 2,
                                               initial_center[1] - self.image.get_rect().height / 2)

    def get_image(self):
        return self.image

    def get_position(self):
        return (self.rect.left, self.rect.top)

    def get_center(self):
        return self.rect.center

    def get_width(self):
        return self.rect.width

    def get_height(self):
        return self.rect.height

    def update(self, dx, dy):
        self.rect.move_ip(dx, dy)
       
class SpriteSheet:
    """
    A collection of game's graphics
    """
    def __init__(self, path, resolution, width, height):
        """
        param path : path to the spritsheet
        type path : string
        param resolution : spritesheet's resolution
        type resolution : int
        param width:
        type width: int
        param width:
        type width: int
        """
        self.sprites = []
        self.resolution = resolution
        spritesheet = pygame.image.load(path).convert_alpha()
        row = 0
        column = 0
        while row < width / resolution:
            while column < height / resolution:
                left_edge = resolution * column
                top_edge = resolution * row
                rect = pygame.Rect(left_edge, top_edge, resolution, resolution)
                image = pygame.Surface(rect.size).convert_alpha()
                image.blit(spritesheet, (0, 0), rect)
                self.sprites.append(image)
                column += 1
            row += 1
            column = 0

    def get_image(self, index, scale=None):
        """
        Returns the sprite at index 
        """
        if scale is not None:
            sprite = pygame.transform.scale(self.sprites[index], scale)
            return sprite
        else:
            return self.sprites[index]

    def get_resolution(self):
        """
        Returns the native resolution of the spritesheet
        """
        return self.resolution

    def get_size(self):
        """
        Returns the size of the spritesheet
        """
        return len(self.sprites)