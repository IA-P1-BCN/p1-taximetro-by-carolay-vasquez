import threading
import time
import logging


from . import config


logger = logging.getLogger(__name__)



STATE_STOPPED = "stopped"
STATE_MOVING = "moving"


def rate_for_state(state: str) -> float:
    if state == STATE_STOPPED:
        return config.RATE_STOPPED
    if state == STATE_MOVING:
        return config.RATE_MOVING
    logger.error("Unknown state requested: %s", state)
    raise ValueError(f"Unknown state: {state!r}")


def fare_for_segment(state: str, seconds: float) -> float:
    return rate_for_state(state) * seconds


class Ride:
    def __init__(self):
        self.state = STATE_STOPPED
        self.fare = 0.0
        self.active = False
        self.start_time = None
        self._lock = threading.Lock()
        self._thread = None
        self._stop_event = threading.Event()

    def start(self):
        #Start a new ride and launch background accumulator thread
        self.fare = 0.0
        self.state = STATE_STOPPED
        self.active = True
        self.start_time = time.time()
        self._stop_event.clear()
        self._thread = threading.Thread(target=self._accumulate, daemon=True)
        self._thread.start()
        logger.info("Ride started")

    def change_state(self, new_state: str):
        #Change the taxi's current state
        with self._lock:
            old_state = self.state
            self.state = new_state
        logger.info("State changed: %s -> %s", old_state, new_state)

    def finish(self) -> float:
        #Stop the ride, wait for the background thread to fully stop and return the final fare
        self._stop_event.set()
        self._thread.join()
        self.active = False
        logger.info(
            "Ride finished: duration=%.1fs fare=%.2f", self.duration_seconds(), self.fare
        )
        return self.fare

    def duration_seconds(self) -> float:
        #How long this ride has been running, in seconds
        if self.start_time is None:
            return 0.0
        return time.time() - self.start_time

    def current_status(self):
        with self._lock:
            state = self.state
            fare = self.fare
        return state, fare, self.duration_seconds()

    def _accumulate(self):
        #Runs in the background thread (every 0.1s, add the fare accrued during that slice of time)
        last_tick = time.time()
        while not self._stop_event.is_set():
            time.sleep(0.1)
            now = time.time()
            elapsed = now - last_tick
            last_tick = now
            with self._lock:
                self.fare += fare_for_segment(self.state, elapsed)
