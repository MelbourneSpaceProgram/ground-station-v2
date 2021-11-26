"""This module contains classes that store satellite data."""

from pathlib import Path

from settings import get_data_dir
from skyfield.api import Timescale, load

TLE_DIR = get_data_dir() / "tle"


class Satellite():
    """Wrapper around Skyfield's EarthSatellite.

    Attributes:
      ID   -- the NORAD ID of the satellite
      name -- the name of the satellite
      data -- the loaded EarthSatellite object
    """

    def __init__(self, ID: str, ts: Timescale) -> None:
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
            # REVIEW: what to do if loading TLE fails?
            raise Exception("Failed to load TLE for " + ID)

        # Check if the TLE is out of date
        if abs(ts.now() - self.data.epoch) > 14:
            self.data = load.tle_file(url, filename=filename.as_posix(),
                                      reload=True)[0]

        self.name = self.data.name
