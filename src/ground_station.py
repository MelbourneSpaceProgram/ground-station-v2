"""This module contains the core logic for the ground station."""

import signal
import sys
import time

import settings
from tracker.sat_tracker import SatelliteTracker


class GroundStation():
    """Where everything happens."""

    def __init__(self) -> None:
        """Init the ground station.

        Loads settings from disk and constructs required objects.
        """
        self.running = False

        # Ensure that things are cleaned up if interrupted
        signal.signal(signal.SIGINT, self.clean_up)
        signal.signal(signal.SIGTERM, self.clean_up)

        self.sat_tracker = SatelliteTracker(settings.get("satellites"))

    def start(self) -> None:
        """Start the ground station."""
        self.running = True
        self.run()

    def clean_up(self, signal, frame) -> None:  # type: ignore
        """Ensure resources are closed before exiting."""
        print("Cleaning up")
        sys.exit(0)

    def run(self) -> None:
        """Run the ground station."""
        while(self.running):
            print("Running")
            self.sat_tracker.update()
            time.sleep(1)
