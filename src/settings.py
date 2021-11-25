"""Maintains the settings.json file.

Reads this file when starting up the ground station and keeps it updated as
changes occur.

Options (TODO):
- Position of ground station (longitude/latitude)
- Satellites to track (use NORAD ID?)
"""


import json
from typing import Any, Dict

from utils import get_root_dir, get_data_dir


DEFAULT_SETTINGS_FILE = get_root_dir() / "default.json"
SETTINGS_FILE = get_data_dir() / "settings.json"

_cache: Dict[str, Any] = {}


def _load_settings() -> Dict[str, Any]:
    path = SETTINGS_FILE if SETTINGS_FILE.exists() else DEFAULT_SETTINGS_FILE
    with open(path, 'r') as file:
        return json.load(file)


def get(key: str) -> Dict[str, Any]:
    """Retrieve the given setting."""
    global _cache
    if not _cache:
        _cache = _load_settings()
    return _cache[key]


def set(key: str, value: Any) -> None:
    """Set the given setting to the specified value.

    Only works for top-level keys.
    """
    global _cache
    if not _cache:
        _cache = _load_settings()
    _cache[key] = value

    # Write changes to file
    with open(SETTINGS_FILE, 'w') as file:
        json.dump(_cache, file, indent=2)
