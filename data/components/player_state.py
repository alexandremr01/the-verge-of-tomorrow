
# Events
BLEED_EVENT = 1
SLOW_EVENT = 2
RUN_EVENT = 3
STOP_RUN_EVENT = 4
STRONGER_EVENT = 5
TIRED_EVENT = 6
STOP_BLEEDING_EVENT = 8
STOP_SLOW_EVENT = 9

MAX_RUNNING_TIME = 2000
MAX_BLEEDING_TIME = 4000
BLEEDING_INTERVAL = 1000
MAX_SLOW_TIME = 5000
TIRED_TIME = 3000

BLEEDING_DAMAGE = 0.5

class PlayerStateFSM:
    def __init__(self):
        self._state = NeutralState()
        pass

    def get_state_name(self):
        return self._state.get_name()

    def get_state(self):
        return type(self._state)

    def send_event(self, event, time):
        # print(" Recebi "+str(event))
        next_state = self._state.send_event(event, time)
        # print(" Indo para "+str(next_state))

        if next_state != None:
            # print(" Indo para " + str(next_state.get_name()))
            self._state = next_state

    def update(self, time):
        next_state = self._state.update(time)
        if next_state != None:
            self._state = next_state

class State:
    def send_event(self, event, time):
        return None

    def update(self, time):
        return None

    def get_name(self):
        return "Null"

class NeutralState(State) :
    def send_event(self, event, time):
        if event == RUN_EVENT:
            return RunningState(time)
        if event == BLEED_EVENT:
            return BleedingState(time)
        if event == SLOW_EVENT:
            return SlowState(time)
    def get_name(self):
        return "Neutral"

class TiredState(State) :
    def __init__(self, time):
        self.start_time = time

    def update(self, time):
        if time - self.start_time > TIRED_TIME:
            return NeutralState()
        return None

    def send_event(self, event, time):
        if event == STOP_RUN_EVENT:
            return TiredState(time)
        if event == BLEED_EVENT:
            return BleedingState(time)
        if event == SLOW_EVENT:
            return SlowState(time)

    def get_name(self):
        return "Tired"

class RunningState(State):
    def __init__(self, time):
        self.start_time = time

    def send_event(self, event, time):
        if event == STOP_RUN_EVENT:
            return TiredState(time)

    def update(self, time):
        if time - self.start_time > MAX_RUNNING_TIME:
            return TiredState(time)
        return None

    def get_name(self):
        return "Running"

class BleedingState(State):
    def __init__(self, time):
        self.start_time = time

    def send_event(self, event, time):
        if event == STOP_BLEEDING_EVENT:
            return NeutralState()


    def update(self, time):
        if time - self.start_time > MAX_BLEEDING_TIME:
            return NeutralState()
        return None

    def get_name(self):
        return "Bleeding"

class SlowState(State):
    def __init__(self, time):
        self.start_time = time

    def send_event(self, event, time):
        if event == STOP_SLOW_EVENT:
            return NeutralState()

    def update(self, time):
        if time - self.start_time > MAX_SLOW_TIME:
            return NeutralState()
        return None

    def get_name(self):
        return "Slow"