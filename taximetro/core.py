import time
from . import config


STATE_STOPPED = "stopped"
STATE_MOVING = "moving"


def rate_for_state(state: str) -> float:
    if state == STATE_STOPPED:
        return config.RATE_STOPPED
    if state == STATE_MOVING:
        return config.RATE_MOVING
    raise ValueError(f"Unknown state: {state!r}")


def fare_for_segment(state: str, seconds: float) -> float:
    return rate_for_state(state) * seconds


class Ride:
    def __init__(self):
        self.state = STATE_STOPPED
        self.fare = 0.0
        self.active = False
        self._last_change = None

    def start(self):
        #Start a new ride, with the fare reset to 0
        self.fare = 0.0
        self.state = STATE_STOPPED
        self.active = True
        self._last_change = time.time()

    def change_state(self, new_state: str):
        #Change the taxi's state, settling the previous segment first
        now = time.time()
        elapsed = now - self._last_change
        self.fare += fare_for_segment(self.state, elapsed)
        self.state = new_state
        self._last_change = now

    def finish(self) -> float:
        #Close the ride, settle the last segment and return the total
        now = time.time()
        elapsed = now - self._last_change
        self.fare += fare_for_segment(self.state, elapsed)
        self.active = False
        return self.fare