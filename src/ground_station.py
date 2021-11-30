"""This module contains the core logic for the ground station."""

import signal
import sys
import time
from timeit import default_timer as timer

from tracker.sat_tracker import SatelliteTracker


class GroundStation():
    """Where everything happens."""

    def __init__(self) -> None:
        """Init the ground station."""
        self.running = False

        # Ensure that things are cleaned up if interrupted
        signal.signal(signal.SIGINT, self.clean_up)
        signal.signal(signal.SIGTERM, self.clean_up)

        self.sat_tracker = SatelliteTracker()

    def start(self) -> None:
        """Start the ground station."""
        self.running = True
        self.curr_time = timer()
        self.run()

    def clean_up(self, signal, frame) -> None:  # type: ignore
        """Ensure resources are closed before exiting."""
        print("Cleaning up")
        sys.exit(0)

    def run(self) -> None:
        """Run the ground station."""
        while(self.running):
            print("Running")
            elapsed = timer() - self.curr_time
            print(elapsed)
            self.curr_time = timer()
            self.sat_tracker.update()
            time.sleep(1)
