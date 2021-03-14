"""
Class that abstracs a generic entity of the game, anything
that is drawed onto the screen.
"""

from .sprite import Sprite

class Entity:
    """
    Anything that has position and an image.
    """
    def __init__(self, position, sprite_graphic):
        self.sprite = Sprite(position, sprite_graphic)

    def update_sprite(self, sprite_graphic):
        self.sprite = Sprite(self.get_position(), sprite_graphic)

    def get_position(self):
        """
        Returns its center position
        """
        return self.sprite.rect.center

    def set_center_position(self, x, y):
        """
        Moves its image to position (x, y)
        """
        self.sprite.rect.update(x - self.sprite.rect.width/2, y - self.sprite.rect.height/2
                                , self.sprite.rect.width, self.sprite.rect.height)

    def move(self, d_x, d_y):
        """
        Moves its image d_x units left and d_y units down
        """
        self.sprite.rect.move_ip(d_x, d_y)

    def draw(self, surface, screen_pos):
        """
        Draws this entity in its current position,
        on surface, a pygame Surface
        """
        surface.blit(self.sprite.get_image(), self.sprite.get_position() - screen_pos)
