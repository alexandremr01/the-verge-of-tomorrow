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

    def update(self, event):
        """
        Gives information to current state, make decision based on it
        and then draw the final state decided
        """
        self.current_state.handle_event(event)
        self.update_state()
        self.current_state.draw()

    def update_state(self):
        """
        Updates to the new state defined by the current state class
        """
        if self.current_state.next is not None:
            self.previous_state = self.current_state
            self.current_state = self.states_dict[self.previous_state.next]
