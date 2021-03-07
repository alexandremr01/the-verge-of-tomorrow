"""
Class that abstracs a generic entity of the game, anything
that is drawed onto the screen.
"""

class Entity:
    """
    Anything that has position and an image.
    """
    def __init__(self, position, sprite):
        """
        param position:
        param sprite: Sprite
        """
        self.position = position
        self.sprite = sprite
