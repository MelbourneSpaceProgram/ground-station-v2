#!/usr/bin/env python3

from pathlib import Path


def get_root_dir() -> Path:
    """Return the root directory of the project."""
    return Path(__file__).absolute().parent.parent
