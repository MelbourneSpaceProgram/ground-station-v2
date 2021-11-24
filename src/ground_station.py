#!/usr/bin/env python3
"""The main controller of the ground station."""


import signal
import sys
import time

import settings


class GroundStation():
    def __init__(self) -> None:
        self.running = False
        signal.signal(signal.SIGINT, self.clean_up)
        signal.signal(signal.SIGTERM, self.clean_up)

    def start(self) -> None:
        self.running = True
        print(settings.get_location())

        settings.set_location("Adelaide")
        print(settings.get_location())

        self.run()

    def clean_up(self, signal, frame) -> None:  # type: ignore
        print("Cleaning up")
        sys.exit(0)

    def run(self) -> None:
        while(self.running):
            print("Running")
            time.sleep(1)
