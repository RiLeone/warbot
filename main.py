#!/usr/bin/env python3
"""
    WarBot: Run a Full (Simulated) Game
    ===================================

    Command-line options:
        -v  verbose     give details about battles

"""

import sys
import matplotlib.pyplot as pltlib

sys.path.append("src/")

import WarBot
import WorldSelector
import AuxiliaryTools
import HistoricStatistician as hs



def main():
    """Run the full game."""

    pltlib.rc("figure", figsize = (16, 9))

    print(__doc__)
    options = AuxiliaryTools.parse_args()

    world_file = WorldSelector.select_world()
    wb = WarBot.WarBot(world_file)
    wb.run(**options["WarBot.run"])

    statistician = hs.HistStat(wb.get_history())
    stat_res = statistician.run()

    pltlib.show()



if __name__ == "__main__":
    main()
