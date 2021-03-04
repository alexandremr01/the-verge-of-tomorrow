"""
Implementation of a state machine to handle screens
like selection, title and scores
"""

class StateMachine:
    """
    State machine that handles screen change in game
    """
    def __init__(self, states_dict, initial_state):
        self.states_dict = states_dict
        self.current_state = initial_state
        self.previous_state = None

    def update(self, events, keys):
        """
        Gives information to current state, make decision based on it
        and then updates state if the current state decided to do so
        """
        self.current_state.handle_input(events, keys)
        self.update_state()

    def update_state(self):
        """
        Updates to the new state defined by the current state class
        """
        self.current_state.update()

        if self.current_state.next is not None:
            self.previous_state = self.current_state
            self.current_state = self.states_dict[self.previous_state.next]

    def draw_current(self, surface):
        """
        Draws the current state on surface
        """
        self.current_state.draw(surface)
