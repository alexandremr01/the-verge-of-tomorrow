"""
This is an interface not supposed to be instantiated
directly. Instead, one of its derivate classes should be
"""

class State:
    """
    Prototype class, not meant to be instantiated. It represents
    a given possible screen mode in the game, which are managed
    by the state machine class
    """
    def __init__(self):
        self.next = None
        self.clear_window = False
        self.custom_value = None

    def update(self):
        """
        Updates the elements of this state through time,
        should be overloaded in children, unless if it is
        a static image
        """

    def draw(self, screen):
        """
        Draws this state on surface, should be overloaded
        """

    def handle_input(self, events, keys):
        """
        Updates its elements based on a given input by user,
        in the form of pygame events and keys, should be
        overloaded
        """
