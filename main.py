#!/usr/bin/env python3
"""
    WarBot: Run a Full (Simulated) Game
    ===================================

    Command-line options:
        -v  verbose     give details about battles

"""

import sys

sys.path.append("src/")

import WarBot
import WorldSelector
import AuxiliaryTools
import HistoricStatistician as hs



def main():
    """Run the full game."""

    print(__doc__)
    options = AuxiliaryTools.parse_args()

    world_file = WorldSelector.select_world()
    wb = WarBot.WarBot(world_file)
    wb.run(**options["WarBot.run"])



if __name__ == "__main__":
    main()
