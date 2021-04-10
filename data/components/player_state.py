from ..constants import ZOMBIE_HEALTH, PLAYER_INITIAL_VELOCITY

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

MAX_STRONG_RUNNING_TIME = 5000
MAX_STRONG_TIME = 10000

BLEEDING_DAMAGE = 0.5


class PlayerStateFSM:
    def __init__(self):
        self._state = NeutralState()
        pass

    def get_state_name(self):
        return self._state.get_name()

    def get_state(self):
        return type(self._state)

    def get_damage(self, original_damage):
        return self._state.get_damage(original_damage)

    def get_velocity(self):
        return self._state.get_velocity()

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

    def get_damage(self, original_damage):
        return original_damage

    def get_velocity(self):
        return PLAYER_INITIAL_VELOCITY


class NeutralState(State):
    def send_event(self, event, time):
        if event == RUN_EVENT:
            return RunningState(time)
        if event == BLEED_EVENT:
            return BleedingState(time)
        if event == SLOW_EVENT:
            return SlowState(time)
        if event == STRONGER_EVENT:
            return StrongState(time)

    def get_name(self):
        return "Neutral"


class TiredState(State):
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

    def get_velocity(self):
        return 2.0 * PLAYER_INITIAL_VELOCITY


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

    def get_velocity(self):
        return 0.5 * PLAYER_INITIAL_VELOCITY


class StrongState(State):
    def __init__(self, time):
        self.start_time = time

    def send_event(self, event, time):
        if event == RUN_EVENT:
            return StrongRunState(time, self.start_time)

    def update(self, time):
        if time - self.start_time > MAX_STRONG_TIME:
            return NeutralState()
        return None

    def get_name(self):
        return "Strong"

    def get_damage(self, original_damage):
        return ZOMBIE_HEALTH


class StrongRunState(State):
    def __init__(self, time, start_strong_time):
        self.start_time = time
        self.start_strong_time = start_strong_time

    def send_event(self, event, time):
        if event == STOP_RUN_EVENT:
            return StrongState(time)

    def update(self, time):
        if time - self.start_time > MAX_STRONG_RUNNING_TIME:
            return StrongState(self.start_strong_time)
        if time - self.start_strong_time > MAX_STRONG_TIME:
            return NeutralState()
        return None

    def get_name(self):
        return "Running"

    def get_damage(self, original_damage):
        return ZOMBIE_HEALTH

    def get_velocity(self):
        return 2.0 * PLAYER_INITIAL_VELOCITY
