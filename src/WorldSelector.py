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
    """Select world from a list.

    Selection can be done by index (the one in the printed list) or name of the
    detected worlds. Worlds need to be in the worlds/ folder and feature a
    states.json file.

    """

    dnames = list_worlds(root)
    print("World-selection. Plese select a world, choose from: ")
    for ii, dn in enumerate(dnames):
        try:
            print("\t{}. {}".format(ii + 1, get_last_part_of_path(dn)))

        except:
            pass

    choice = input("\nSelect by name or number (int) [Default: 1. {}]: ".format(
        get_last_part_of_path(dnames[0])
        )
    )
    print()

    return verify_choice(root, dnames, choice)


def verify_choice(root: str, dnames: list, choice: str) -> str:
    """Verify that the choice is valid."""

    default = "/".join((root, WORLDS_FOLDER, DEFAULT_WORLD, DEFAULT_FILENAME))

    try:
        idx = int(choice) - 1
        sel = dnames[idx] if idx >= 0 and idx < len(dnames) else DEFAULT_WORLD
        selected = "/".join((root, WORLDS_FOLDER, sel, DEFAULT_FILENAME))

    except:
        selected = "/".join((root, WORLDS_FOLDER, choice, DEFAULT_FILENAME))

    if os.path.exists(selected) and os.path.isfile(selected):
        return selected

    else:
        return default


def list_worlds(root: str) -> list:
    """List the worlds from which one can choose."""

    pname, dnames, fnames = next(os.walk("/".join((root, WORLDS_FOLDER))))
    return dnames.copy()


def get_last_part_of_path(path: str) -> str:
    """Return the last part of a path string (subdir or file) as a string."""

    return path.split("/")[-1]



if __name__ == "__main__":
    print(__doc__)

    file_path = select_world(".")
    print(file_path)
