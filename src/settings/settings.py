#!/usr/bin/env python3
"""Maintains the settings.yml file.

Reads this file when starting up the ground station and keeps it updated as
changes occur.

What should the format look like?
"""

import yaml
from utils import get_root_dir


class Settings():
    SETTINGS_FILE = get_root_dir() / "settings.yml"

    def __init__(self):
        with open(self.SETTINGS_FILE, 'r') as settings:
            self.data = yaml.load(settings, yaml.Loader)

    def print(self):
        print("Dumping settings.yml")
        print(yaml.dump(self.data))
