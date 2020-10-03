#!/usr/bin/env python3
"""
    WarBot: Run a Full (Simulated) Game
    ===================================

    Command-line options:
        -v  verbose     give details about battles

"""

import sys
import pprint
import matplotlib.pyplot as pltlib

sys.path.append("src/")

import WarBot
import WorldSelector
import AuxiliaryTools
import HistoricStatistician as hs



def main():
    """Run the full game."""

    AuxiliaryTools.setup_matplotlib_options(**AuxiliaryTools.DEFAULT_MATPLOTLIB_OPTIONS)

    print(__doc__)
    options = AuxiliaryTools.parse_args()

    world_file = WorldSelector.select_world()
    wb = WarBot.WarBot(world_file)
    wb.run(**options["WarBot.run"])

    statistician = hs.HistStat(wb.get_history())
    stat_res = statistician.run()
    statistician.print_results()

    print("\n*** End of simulation - Close figure to exit program. ***\n")
    pltlib.show()



if __name__ == "__main__":
    main()
