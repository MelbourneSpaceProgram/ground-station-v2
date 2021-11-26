"""This module contains the logic for tracking satellite passes."""

from typing import Dict, Tuple

from datetime import timedelta
import pytz  # type: ignore
import settings
from skyfield.api import load, wgs84, Time

from .sat import Satellite


class SatelliteTracker():
    """Tracks the position of satellites and manages their events.

    Attributes:
      sats -- a dict of satellites currently being tracked using
              their NORAD ID as keys
      ts   -- Skyfield's timescale object (manages conversions
              between different timescales)
      tz   -- the timezone of the ground station
      passes   -- a dict of next passes for tracked satellites
      min_alt  -- the minimum altitude in degrees of a pass
      ground_station -- the position of the ground station
    """

    def __init__(self) -> None:
        """Init tracker with data of tracked satellites.

        Arguments:
          sats: a list of NORAD IDs
          lat: latitude of the ground station
          lon: longitude of the ground station
        """
        # Init timescale
        self.ts = load.timescale()

        # Init ground station position
        lat = settings.get("lat")
        lon = settings.get("lon")
        # REVIEW: need to specify elevation?
        self.ground_station = wgs84.latlon(lat, lon)

        # Init timezone
        tz = settings.get("timezone")
        self.tz = pytz.timezone(tz)

        # Init min_alt
        self.min_alt = settings.get("min_alt")

        # Load satellites
        self.sats: Dict[str, Satellite] = {}
        self.passes: Dict[str, Tuple[Time, Time]] = {}
        for ID in settings.get("satellites"):
            sat = Satellite(ID, self.ts)
            self.sats[ID] = sat
            self.passes[ID] = self.compute_next_pass(sat)

        print("Loaded: " + ", ".join([ID for ID in self.sats.keys()]))

    def add_satellite(self, ID: str) -> None:
        """Add satellite to tracking list."""
        sat = Satellite(ID, self.ts)
        self.sats[ID] = sat
        settings.set("satellites", self.sats.keys())

    def remove_satellite(self, ID: str) -> None:
        """Remove satellite from tracking list."""
        self.sats.pop(ID)
        settings.set("satellites", self.sats.keys())

    def compute_next_pass(self, sat: Satellite) -> Tuple[Time, Time]:
        """Compute the times when the satellite will rise and set next."""
        start = self.ts.now()
        # REVIEW: Search over the next 24 hours (is this sufficient?)
        end = self.ts.utc(start.utc_datetime() + timedelta(days=1))

        times, events = sat.data.find_events(self.ground_station, start, end,
                                             altitude_degrees=self.min_alt)

        # event: 0 (rise), 1 (culminate), 2 (set)
        rise_t = times[next(i for i, event in enumerate(events) if event == 0)]
        set_t = times[next(i for i, event in enumerate(events) if event == 2)]

        return (rise_t, set_t)

    def timestamp(self, time: Time) -> str:
        """Convert a time to a string."""
        # TODO: move into utils?
        dt = time.astimezone(self.tz)
        return dt.strftime("%y/%m/%d-%H:%M:%S")

    def update(self) -> None:
        """Update satellites and check for events."""
        print("Tracking")
        for ID, (rise_t, set_t) in self.passes.items():
            print(ID + ": " + self.timestamp(rise_t) + ", " +
                  self.timestamp(set_t))
