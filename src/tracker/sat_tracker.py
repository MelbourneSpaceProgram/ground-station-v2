"""This module contains the logic for tracking satellite passes."""

from typing import Dict, List
from .sat import Satellite


class SatelliteTracker():
    """Tracks the position of satellites and manages their events.

    Attributes:
      sats: a dict of satellites currently being tracked using their
            NORAD ID as keys
    """

    def __init__(self, sats: List[str]) -> None:
        """Init tracker with data of tracked satellites."""
        self.sats: Dict[str, Satellite] = {}
        for ID in sats:
            sat = Satellite(ID)
            self.sats[ID] = sat
        print(str(sats))

    def add_satellite(self, name: str, ID: str) -> None:
        """Add satellite to tracking list."""
        sat = Satellite(ID)
        self.sats[ID] = sat

    def remove_satellite(self, ID: str) -> None:
        """Remove satellite from tracking list."""
        self.sats.pop(ID)

    def update(self) -> None:
        """Update satellites and check for events."""
        print("Tracking")
