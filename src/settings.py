"""Maintains the settings.json file.

Reads this file when starting up the ground station and keeps it updated as
changes occur.

Options:
- Position of ground station (longitude/latitude)
- Satellites to track (use NORAD ID?)
"""


import json

from utils import get_root_dir

SETTINGS_FILE = get_root_dir() / "settings.json"


def get_location() -> str:
    with open(SETTINGS_FILE, 'r') as file:
        data = json.load(file)
        return data["location"]


def set_location(location: str) -> None:
    with open(SETTINGS_FILE, 'r+') as file:
        data = json.load(file)

        data["location"] = location

        # Overwrite settings
        file.seek(0)
        json.dump(data, file, indent=2)
        file.truncate()
