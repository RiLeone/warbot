#!/usr/bin/env python3
"""
    WarBot Main Object Source
    =========================


"""

import copy
import json
import pprint
import logging
import numpy as np
from datetime import datetime
import matplotlib.pyplot as pltlib

import State
import AuxiliaryTools


logger = AuxiliaryTools.setup_logging(__name__, local_level = logging.INFO)
YEAR = datetime.now().year
MAX_PARALLEL_BATTLES = 1


class WarBot:
    """WarBot Object

    This is the main object in the game: it loads start properties of the world
    of interest, computes rounds and saves the history. The bare minimum code to
    let it run is the following

    wb = WarBot(<path_to_json_file>)
    wb.run()

    where <path_to_json_file> is a string indicating the path to a JSON file
    with the structure

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

    see for example <prj_root>/Switzerland/states.json.

    """

    def __init__(self, data_file: str) -> "WarBot Object":
        self._players = State.load_states_from_json_file(data_file)
        self._players_names = [pn.replace("_", " ").capitalize() for pn in self._players.keys()]
        self._world_population = self.compute_world_population()
        self._year = YEAR
        self._n_battles = 0
        self._global_fatalities = 0
        self._global_pop_increase = 0

        self._history = {
            "year": [YEAR, ],
            "states": [self._players_names.copy(), ],
            "n_of_states": [len(self._players_names), ],
            "world_population": [self._world_population, ],
            "n_of_battles": [0, ],
            "n_of_fatalities": [0, ],
            "n_of_pop_increse": [0, ],
        }
        self._n_of_rounds = 0
        self._max_rounds = len(self._players.keys())

        self._losers = []


    def compute_round(self):
        """Compute/simulate a single round of the game.

        This involves getting a list of pairs of battling states (have to be
        neighboring states) and computing the outcomes of the battles.
        """

        battle_pairs = self.get_pairs()
        self.compute_battles(battle_pairs)
        self._players_names = list(self._players.keys())
        self._n_of_rounds += 1


    def get_pairs(self) -> list:
        """Get battling pairs.

        From the current state of the world, pick neighboring states which will
        have a fight in this round. This method returns a list of lists of
        neighboring states (randomly selected).

        NOTE: so far only one pair is selected at each round. Also, it was
        thought that a state can only have one adversary at the time. This
        mechanic might as well be dropped/changed for more 'interesting' plots
        of the world history.
        """

        pairs = []
        available_players = list(self._players.keys())
        busy_players = []

        for ii in range(MAX_PARALLEL_BATTLES):
            if len(available_players) > 0:
                idx = np.random.randint(0, len(available_players))

            else:
                break

            p1 = available_players[idx]
            if p1 in busy_players:
                continue

            else:
                available_players.remove(p1)
                busy_players.append(p1)

            available_neighbors = self._players[p1].get_neighbors()

            for bp in busy_players:
                try:
                    available_neighbors.remove(bp)

                except:
                    pass

            if len(available_neighbors) > 0:
                p2 = available_neighbors[np.random.randint(0, len(available_neighbors))]
                busy_players.append(p2)
                pairs.append([p1, p2])

            else:
                busy_players.remove(p1)

        return pairs


    def compute_battles(self, battle_pairs: list):
        """Compute the outcome of all battles specified by the battle_pairs.

        One way of getting battle pairs is to call the get_pairs() method. All
        states NOT involved in battles grow in population according to their
        growth-rate.
        """

        fatalities = 0
        winners = []
        losers = []
        for pp in battle_pairs:
            strengths = self.compute_battle_strengths(
                [self._players[p] for p in pp],
                method = "poparea"
            )

            result = np.random.rand(1)

            if result > strengths[0]:
                winner = pp[0]
                loser = pp[1]

            else:
                winner = pp[1]
                loser = pp[0]

            pop_losses = [self.compute_fatalities(self._players[p].get_population(),
                rs, result) for p, rs in zip(pp, strengths)]
            self.update_populations_after_battle(pp, pop_losses)
            for pl in pop_losses:
                fatalities += pl

            losers.append(loser)
            winners.append(winner)

            logger.info("BATLLE INFO :: Battle between {:s} and {:s} was won by {:s}.".format(pp[0], pp[1], winner))
            logger.info("BATLLE INFO :: Fatalities: {:s}: {:d} \t {:s}: {:d}.".format(pp[0], pop_losses[0], pp[1], pop_losses[1]))

        for w, l in zip(winners, losers):
            self.merge_players(w, l)

        self.clean_neighborhoods(losers, winners)
        self._losers += losers

        battling_states = winners + losers
        self.update_populations_of_non_battling_states(battling_states)

        self._global_fatalities = fatalities
        self._n_battles = len(battle_pairs)


    def update_populations_after_battle(self, players_keys: list, pop_losses: list):
        """Update the population values after the battle"""

        for pk, pl in zip(players_keys, pop_losses):
            self._players[pk].update_population_after_battle(pl)


    def update_populations_of_non_battling_states(self, battling_states: list):
        """Update populations of non battling states."""

        global_increase = 0
        for sn, pp in self._players.items():
            if not sn in battling_states:
                delta_p = pp.grow()
                global_increase += delta_p

        self._global_pop_increase = global_increase


    def clean_neighborhoods(self, losers: list, winners: list):
        """Update the world after the battles are over in terms of neighborhoods."""

        for p in self._players.keys():
            original_hood = self._players[p].get_neighbors()
            self._players[p].clean_neighborhood(losers)
            for w, l in zip(winners, losers):
                if l in original_hood and w not in self._players[p].get_neighbors():
                    self._players[p].add_neighbor(w)


    def merge_players(self, winner: str, loser: str):
        """Merge losers into winners for each battle."""

        self._players[winner].merge_with(self._players[loser])
        del self._players[loser]


    def run(self, verbose: bool = False):
        """Run a game.

        This is the one method to call them all. It simulates the full game
        until there is either only one state left or the max number of
        iterations has been reached.
        """

        print_command = logger.warning

        if verbose:
            print_command = print

        counter = 0
        while self._n_of_rounds < self._max_rounds and len(self._players_names) > 1:
            print_command("HISTORY INFO :: Number of remaining states {:d}".format(len(list(self._players.keys()))))
            print_command("HISTORY INFO :: Round {:d} being computed...".format(counter))
            counter += 1
            self._year += 1
            self.compute_round()
            self._world_population = self.compute_world_population()

            self.update_history()
            self.print_players()


    def update_history(self):
        """Update history by appending latest values"""

        self._history["year"].append(self._year)
        self._history["states"].append(self._players_names.copy())
        self._history["n_of_states"].append(len(self._players_names))
        self._history["world_population"].append(self._world_population)
        self._history["n_of_battles"].append(self._n_battles)
        self._history["n_of_fatalities"].append(self._global_fatalities)
        self._history["n_of_pop_increse"].append(self._global_pop_increase)


    def get_history(self):
        """Get history safely"""

        return copy.deepcopy(self._history)


    def print_players(self):
        """Auxiliary method for (pretty) printing the remaining states."""

        print("* Year {:d}, Surviving states are:".format(self._year))
        for state_name, state in self._players.items():
            print("\t{:s}: Population {:d}, Area {:d} km2, Neighbors: {}".format(
                state_name.capitalize(),
                state.get_population(),
                state.get_area(),
                state.get_neighbors()
                )
            )

        print()
        print("\tTotal World Population: {:d}\n".format(self._world_population))


    def compute_world_population(self) -> int:
        """Compute world population."""

        return sum([st.get_population() for st in self._players.values()])


    @staticmethod
    def compute_battle_strengths(battle_pair: list, method: str = "poparea") -> list:
        """Given a battle pair compute the relative strenghts of the contestants
        and return them in a list of floats.

        <battle_pair> is a list of State-objects

        <method> is a string in ("poparea", ). If an invalid <method> is
        provided, "poparea" is used. Default method is "poparea".
        """

        strengths = [bp.compute_battle_strength(method) for bp in battle_pair]

        tot_s = np.sum(strengths)
        strengths = list(map(lambda x: x / tot_s, strengths))

        return strengths


    @staticmethod
    def compute_fatalities(pop: int, rel_strength: float, battle_outcome: float) -> int:
        """Compute fatalities occurred in battle

        The fatalities depend on the available population <pop>, the relative
        strength of the player <rel_strengt> [0, 1], and the battle outcome
        <battle_outcome> [0, 1]. Function returns at most pop - 1.

        Rationale:
            1. The loss in population is smaller, the stronger the state is,
               from here:
                    loss ~ 1 - rel_strength.
            2. The loss is higher, the closer the battle outcome was, relative
               to the strength, from here:
                    loss ~ 1 - abs(rel_strengt - battle_outcome)

        """

        return min(
            [
                int(pop * (1 - rel_strength) * (1 - abs(rel_strength - battle_outcome))),
                pop - 1
            ]
        )



if __name__ == "__main__":
    print("\033c")
    print(__doc__)
    print()

    data = "../worlds/Debugland/states.json"
    wb = WarBot(data)
    wb.run(verbose = False)

    hist = wb.get_history()
    print(hist)
