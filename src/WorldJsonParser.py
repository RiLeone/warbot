#!/usr/bin/env python3
"""
    Parse a World Json File
    =====================

    TODO

"""

import copy
import json


class WorldJsonParser:
    """WorldJsonParser Object

    This class loads and parse all the attributes of a json file of the form

    {
        "source": str,
        "states": {
            "state1": {
                "pop": int,
                "area": int or float,
                "id": int (unique),
                "neighbors": [str]
            },
            ...
        }
    }

    See for example <prj_root>/Switzerland/states.json.

    """

    def __init__(self, data_file: str) -> "WorldJsonParser Object":
        with open(data_file, "r") as fp:
            self._states = copy.deepcopy(json.load(fp)["states"])

    def graphNodes(self):
        nodes = []
        for s in self._states:
            for n in self._states[s]["neighbors"]:
                nodes.append((s, n))
        return nodes


if __name__ == "__main__":
    print(__doc__)
    wjp = WorldJsonParser("../worlds/Debugland/states.json")
    print(wjp.graphNodes())
