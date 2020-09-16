#!/usr/bin/env python3
"""
    WorldSelector
    =============

"""

import os
import sys

DEFAULT_FILENAME = "states.json"
WORLDS_FOLDER = "worlds"
DEFAULT_WORLD = "Debugland"


def select_world(root: str = ".") -> str:
    """Select world from a list."""

    res = "/".join((root, WORLDS_FOLDER, DEFAULT_WORLD, DEFAULT_FILENAME))

    return res



if __name__ == "__main__":
    print(__doc__)

    file_path = select_world()
    print(file_path)
