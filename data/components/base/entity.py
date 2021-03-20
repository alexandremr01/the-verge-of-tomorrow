"""
Class that abstracs a generic entity of the game, anything
that is drawed onto the screen.
"""

import numpy as np

from .sprite import Sprite

class Entity:
    """
    Anything that has position and an image.
    """
    def __init__(self, position, sprite_graphic, angle=None):
        self.position = np.array(position)
        if angle is None:
            self.sprite = Sprite(position, sprite_graphic)
        else:
            self.sprite = Sprite(position, sprite_graphic, angle)

    def update_sprite(self, sprite_graphic, angle=None):
        """
        Changes current sprite of entity to the
        new sprite_graphic
        """
        if angle is None:
            self.sprite = Sprite(self.position, sprite_graphic)
        else:
            self.sprite = Sprite(self.position, sprite_graphic, angle)

    def get_position(self):
        """
        Returns its center position
        """
        return np.array(self.sprite.rect.center)

    def move(self, d_x, d_y):
        """
        Moves its image d_x units right and d_y units down
        """
        self.sprite.rect.move_ip(d_x, d_y)
        self.position = np.array(self.sprite.rect.center)

    def draw(self, screen):
        """
        Draws this entity in its current position,
        on surface, a pygame Surface
        """
        screen.blit(self.sprite.get_image(), self.sprite.get_position())
