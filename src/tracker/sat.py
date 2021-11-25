"""This module contains classes that store satellite data."""

from enum import Enum
from pathlib import Path

from skyfield.api import load
from utils import get_root_dir

TLE_DIR = get_root_dir() / "tle"


class Satellite():
    """Wrapper around Skyfield's EarthSatellites.

    Attributes:
      name -- the name of the satellite
      ID   -- the NORAD ID of the satellite
      data -- the loaded EarthSatellite object
    """

    def __init__(self, ID: str) -> None:
        """Init satellite with a name and ID.

        Checks whether the TLE is up to date and redownloads if necessary. TLEs
        are stored in a folder in the root directory.
        """
        self.ID = ID

        if not TLE_DIR.exists():
            Path.mkdir(TLE_DIR)

        url = f'https://celestrak.com/satcat/tle.php?CATNR={ID}'
        filename = TLE_DIR / f'{ID}.txt'

        self.data = load.tle_file(url, filename=filename.as_posix())[0]

        if not self.data:
            raise Exception("Failed to load TLE for " + ID)

        # Check whether we need to redownload the TLE
        ts = load.timescale()
        if abs(ts.now() - self.data.epoch):
            self.data = load.tle_file(url, filename=filename.as_posix(),
                                      reload=True)[0]

        self.name = self.data.name


class SatelliteEvent(Enum):
    """Stores the possible events a satellite can emit."""

    AOS = 1                     # Acquisition of signal
    LOS = 2                     # Loss of signal
    # Could add culmination (when sat is at maximum altitude)
