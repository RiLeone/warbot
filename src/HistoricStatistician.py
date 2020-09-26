#!/usr/bin/env python3
"""
    Historic Statistician
    =====================

    Given the world-history, I will tell you what went down.

"""

import pprint
import numpy as np
import matplotlib.pyplot as pltlib



class HistStat:
    """HistStat

    History statistician compute
    """
    def __init__(self, world_history: dict):
        self._world_history = world_history
        self._line_plot_settings = {
            "ms": 10,
            "lw": 2
        }


    def run(self) -> dict:
        """Run history statistics computation and visualization."""

        res = {}
        res["world_pop_fig"] = self.plot_world_population()
        res["battle_stats"] = self.compute_battle_statistics()

        return res


    def plot_world_population(self) -> pltlib.figure:
        """Plot evolution of world population in the years."""

        xval = self._world_history["year"]
        yval = self._world_history["world_population"]
        fats = self._world_history["n_of_fatalities"]
        growth = self._world_history["n_of_pop_increse"]

        fig = pltlib.figure()
        pltlib.bar(xval[:-1], fats[1:], bottom = np.array(yval[:-1]) - np.array(fats[1:]), ec = "k", fc = "r")
        pltlib.bar(xval[:-1], growth[1:], bottom = yval[:-1], ec = "k", fc = "g")
        pltlib.plot(xval, yval, "ks-", **self._line_plot_settings)
        pltlib.grid(True)
        pltlib.xlabel("Year")
        pltlib.xticks(ticks = xval, labels = ["{:d}".format(xv) for xv in xval])
        pltlib.ylabel("World Population [-]")
        pltlib.ylim((0, 1.1 * max(yval)))

        fig.tight_layout()

        return fig


    def compute_battle_statistics(self) -> dict:
        """Compute battle statistics."""

        battle_stats = {"n_of_battles": None, "n_of_fatalities": None}

        for bsk, bsv in battle_stats.items():
            battle_stats[bsk] = self._world_history[bsk][1:]

        battle_stats["fatalities"] = {
            "avg": round(float(sum(battle_stats["n_of_fatalities"])) / sum(battle_stats["n_of_battles"]), 2)
        }

        return battle_stats



if __name__ == "__main__":
    print(__doc__)

    pltlib.rc("figure", figsize = (16, 9))

    EXAMPLE_HISTORY = {
        'year': [2020, 2021, 2022, 2023],
        'states': [['A', 'B', 'C', 'D'], ['B', 'C', 'D'], ['B', 'C'], ['C']],
        'n_of_states': [4, 3, 2, 1],
        'world_population': [75000, 70145, 55884, 38549],
        'n_of_battles': [0, 1, 1, 1],
        'n_of_fatalities': [0, 5555, 14161, 17335],
        'n_of_pop_increse': [0, 700, -100, 0]
    }

    hs = HistStat(EXAMPLE_HISTORY)
    res = hs.run()

    print("Battle Stats")
    pprint.pprint(res["battle_stats"])

    pltlib.show()
