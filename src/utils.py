"""This module contains useful utility functions."""

from pathlib import Path


def get_root_dir() -> Path:
    """Return the root directory of the project."""
    return Path(__file__).absolute().parent.parent
