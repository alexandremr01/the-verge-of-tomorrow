"""
Contains a spritesheet loader and the base class for a sprite
"""

import pygame

class Sprite(pygame.sprite.Sprite):
    """
    Base class for game's sprite
    """
    def __init__(self, initial_center, sprite_graphic, initial_angle=None, flip=None):
        """
        param sprite_graphic: Sprite's graphics
        type sprite_graphic: pygame.Surface
        param initial_center: sprite's initial center position
        type initial_center: two-dimensional tuple
        """
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface(sprite_graphic.get_rect().size).convert_alpha()
        self.image.set_colorkey((0, 0, 0))
        self.image.blit(sprite_graphic, (0, 0), sprite_graphic.get_rect())
        if initial_angle is not None:
            self.image = pygame.transform.rotozoom(self.image, initial_angle, 1)
            self.image.set_colorkey((0, 0, 0))
        if flip is not None:
            self.image = pygame.transform.flip(self.image, flip[0], flip[1])
        self.rect = self.image.get_rect().move(initial_center[0] - self.image.get_rect().width / 2,
                                               initial_center[1] - self.image.get_rect().height / 2)

    def get_image(self):
        """
        Returns its pygame surface
        """
        return self.image

    def get_position(self):
        """
        Returns its top left corner position
        """
        return (self.rect.left, self.rect.top)

    def get_width(self):
        """
        Returns width
        """
        return self.rect.width

    def get_height(self):
        """
        Returns height
        """
        return self.rect.height

class SpriteSheet:
    """
    A collection of game's graphics
    """
    def __init__(self, path, resolution, width, height):
        """
        param path: path to the spritsheet
        type path: string
        param resolution: spritesheet's resolution
        type resolution: two-dimensional tuple of ints
        param width: width
        type width: int
        param height: height
        type height: int
        """
        self.sprites = []
        self.resolution = resolution
        spritesheet = pygame.image.load(path).convert_alpha()
        row = 0
        column = 0
        while row < height / resolution[1]:
            while column < width / resolution[0]:
                left_edge = resolution[0] * column
                top_edge = resolution[1] * row
                rect = pygame.Rect(left_edge, top_edge, resolution[0], resolution[1])
                image = pygame.Surface(rect.size)
                image.set_colorkey((0, 0, 0))
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
