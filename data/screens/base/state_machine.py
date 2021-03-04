"""
Implementation of a state machine to handle screens
like selection, title and scores
"""

from ...constants import BLACK

class StateMachine:
    """
    State machine that handles screen change in game,
    constructed with a dictionary describing the states
    to manage and its initial_state
    """
    def __init__(self, states_dict, initial_state):
        self.states_dict = states_dict
        self.current_state = self.states_dict[initial_state]
        self.previous_state = None

    def update(self, events, surface):
        """
        Gives information to current state, make decision based on it
        and then updates state if the current state decided to do so,
        drawing it afterwards
        """
        self.current_state.handle_input(events)
        self.update_state(surface)
        self.current_state.draw(surface)

    def update_state(self, surface):
        """
        Updates to the new state defined by the current state class,
        clearing the window if it is set to do so by the current state
        """
        self.current_state.update()

        if self.current_state.next is not None:
            self.previous_state = self.current_state
            self.current_state = self.states_dict[self.previous_state.next]

            if self.previous_state.clear_window is True:
                surface.fill(BLACK)
            self.previous_state.next = None
            self.previous_state.clear_window = False
