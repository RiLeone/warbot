#!/usr/bin/env python3
"""
    ArmiesSelector
    =============

"""

import os

DEFAULT_FILENAME = "armies.json"


def select_armies(world_file) -> str:
    """Select army from a list.
        
    Selection happens automatically based on the selected world. This selector should ideally be called after having 
    selected a world, otherwise default will be taken
    """""

    if os.path.exists(world_file):
        current_path = os.path.dirname(world_file)
        current_file = os.path.join(current_path, DEFAULT_FILENAME)
        return verify_file(current_file)
    else:
        return "."


def verify_file(current_file) -> str:
    if os.path.exists(current_file):
        return current_file
    else:
        return "."


if __name__ == "__main__":
    print(__doc__)

    file_path = select_armies(".")
    print(file_path)
