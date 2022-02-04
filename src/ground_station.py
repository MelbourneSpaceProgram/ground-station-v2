"""This module contains the core logic for the ground station."""

import signal
import sys
import time
from timeit import default_timer as timer
from multiprocessing import Process

# Enable EPS if running on Pi
RUN_EPS = is_raspberrypi()

class GroundStation():
    """Where everything happens."""

    def __init__(self) -> None:
        """Init the ground station."""
        self.running = False

        # Ensure that things are cleaned up if interrupted
        signal.signal(signal.SIGINT, self.clean_up)
        signal.signal(signal.SIGTERM, self.clean_up)

        # Create separate process for EPS script
        if RUN_EPS:
            from EPS import BatteryLoop
            self.EPS = Process(target=BatteryLoop.start(), name="EPS")

    def start(self) -> None:
        """Start the ground station."""

        # Start the EPS process
        if RUN_EPS:
            self.EPS.start()

        self.running = True
        self.curr_time = timer()
        self.run()

    def clean_up(self, signal, frame) -> None:  # type: ignore
        """Ensure resources are closed before exiting."""
        print("Cleaning up")

        if RUN_EPS:
            self.EPS.join()

        sys.exit(0)

    def run(self) -> None:
        """Run the ground station."""
        while(self.running):
            print("Running")
            elapsed = timer() - self.curr_time
            print(elapsed)
            self.curr_time = timer()
            time.sleep(1)


def is_raspberrypi():
    try:
        with io.open('/sys/firmware/devicetree/base/model', 'r') as m:
            if 'raspberry pi' in m.read().lower(): return True
    except Exception: pass
    return False
