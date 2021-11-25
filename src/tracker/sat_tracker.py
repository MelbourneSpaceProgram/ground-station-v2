"""This module contains the logic for tracking satellite passes."""

from typing import Any, Dict

import pytz  # type: ignore
import settings
from skyfield.api import wgs84

from .sat import Satellite


class SatelliteTracker():
    """Tracks the position of satellites and manages their events.

    Attributes:
      sats -- a dict of satellites currently being tracked using
              their NORAD ID as keys
      vecs -- a dict of vectors from the ground station to all
              tracked satellites
      tz   -- the timezone of the ground station
      ground_station
           -- the position of the ground station
    """

    def __init__(self) -> None:
        """Init tracker with data of tracked satellites.

        Arguments:
          sats: a list of NORAD IDs
          lat: latitude of the ground station
          lon: longitude of the ground station
        """
        # Load satellites
        self.sats: Dict[str, Satellite] = {}
        for ID in settings.get("satellites"):
            sat = Satellite(ID)
            self.sats[ID] = sat

        print("Loaded: " + ", ".join([ID for ID in self.sats.keys()]))

        # Init timezone
        tz = settings.get("timezone")
        self.tz = pytz.timezone(tz)

        # Init ground station poisition
        lat = settings.get("lat")
        lon = settings.get("lon")
        self.ground_station = wgs84.latlon(lat, lon)

        # Init vectors
        self.vecs: Dict[str, Any] = {}
        for ID, sat in self.sats.items():
            self.vecs[ID] = sat.data - self.ground_station

    def add_satellite(self, ID: str) -> None:
        """Add satellite to tracking list."""
        sat = Satellite(ID)
        self.sats[ID] = sat
        settings.set("satellites", self.sats.keys())

    def remove_satellite(self, ID: str) -> None:
        """Remove satellite from tracking list."""
        self.sats.pop(ID)
        settings.set("satellites", self.sats.keys())

    def update(self) -> None:
        """Update satellites and check for events."""
        print("Tracking")
